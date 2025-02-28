import asyncio
from typing import Final, Optional

from channels.layers import get_channel_layer  # type: ignore

from ..share import channel_handler, player_data
from ..share import constants as ws_constants
from . import constants as match_constants
from .pong_logic import PongLogic


class MatchManager:
    """
    Pongのゲーム進行・DB操作を担当するクラス

    トーナメント進行クラスに作成され、マッチの進行を行う。
    実際のロジックはPongLogicクラスが担当しこのクラスはそれを操作する。

    Consumerからの入力を関数を通して受け取り、PongLogicインスタンスを操作する。
    60FPSでゲーム情報をChannelLayerを通してConsumerに送信する。

    ChannelLayerのグループ名はf"pong_{match_id}"とする。
    """

    FPS: Final[float] = 1 / 60

    def __init__(
        self,
        match_id: Optional[int],
        player1: player_data.PlayerData,
        player2: player_data.PlayerData,
        mode: str,
    ) -> None:
        """
        Args:
            match_id (int): matchのid
            player1 (player_data.PlayerData): player1の情報
            player2 (player_data.PlayerData): player2の情報
            mode (str): "local" | "remote"のどちらか
        """
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.mode = mode

        self.pong_logic = PongLogic()
        self.group_name = f"pong_{match_id}"  # 一意
        self.ready_players = 0
        self.channel_handler = channel_handler.ChannelHandler(
            get_channel_layer(), None
        )

    async def run(self) -> None:
        """
        この関数を実行することでマッチを実行する。
        このクラスの作成側の関数はこの関数をバックグラウンドタスクとして実行し、終了を待つ。
        """
        # プレーヤーが準備完了のメッセージを送信するのを待つ
        self.wait_message = asyncio.create_task(
            self._wait_for_ready_messages()
        )

        await self.wait_message
        # PongLogic開始
        await self._start_game()

    async def _wait_for_ready_messages(self) -> None:
        """
        以下の人数からreadyメッセージを受け取るのを待つ
        - local mode: 1人
        - remote mode: 2人
        """
        wait_player_num = 1 if self.mode == match_constants.Mode.LOCAL else 2
        while self.ready_players < wait_player_num:
            await asyncio.sleep(0.1)

    async def handle_init_action(self, player: player_data.PlayerData) -> None:
        """
        consumerから渡されたinit メッセージの処理、返信を行う関数。
        consumerから呼び出されるinit actions

        Args:
            player_channel: プレーヤーのchannel_name
        """
        is_remote = (
            True if self.mode == match_constants.Mode.REMOTE.value else False
        )

        message = self._build_message(
            match_constants.Stage.INIT.value,
            {
                match_constants.Team.key(): match_constants.Team.ONE.value
                if player.channel_name == self.player1.channel_name
                else match_constants.Team.ONE.value
                if is_remote
                else None,
                "display_name1": self.player1.participation_name
                if is_remote
                else None,
                "display_name2": self.player2.participation_name
                if is_remote
                else None,
                "paddle1": {
                    "x": self.pong_logic.paddle1_pos.x,
                    "y": self.pong_logic.paddle1_pos.y,
                },
                "paddle2": {
                    "x": self.pong_logic.paddle2_pos.x,
                    "y": self.pong_logic.paddle2_pos.y,
                },
                "ball": {
                    "x": self.pong_logic.ball_pos.x,
                    "y": self.pong_logic.ball_pos.y,
                },
            },
        )
        await self.channel_handler.send_to_consumer(
            message, player.channel_name
        )

    async def handle_ready_action(
        self, player: player_data.PlayerData
    ) -> None:
        """
        consumerから呼び出されるready actions
        consumerから渡されたready メッセージの処理、返信を行う関数。
        """
        # readyメッセージを送ってきたプレーヤーのカウント
        self.ready_players += 1

        # メッセージ作成
        message = self._build_message(
            match_constants.Stage.READY.value,
            {},
        )
        # TODO: もしかしたら2人目が送ってきたタイミングで同時にREADY送らないとかも？
        await self.channel_handler.send_to_consumer(
            message, player.channel_name
        )

    async def _start_game(self) -> None:
        """
        PongLogicの実行を開始し、ゲーム情報を送り続ける関数をバックグラウンドで実行する。
        """
        # TODO: MatchのステータスをON_GOINGに更新

        # PongLogicの実行を開始
        self.send_task = asyncio.create_task(self._send_match_state())

        # send_taskが終わるまで待機
        await self.send_task

        # ゲームが終了したら、Consumerに終了通知を送る
        await self._end_game()

    async def _send_match_state(self) -> None:
        """
        60FPSでPongLogicの状態を更新・取得し、Consumerに送信
        """
        last_update = asyncio.get_event_loop().time()
        while not self.pong_logic.game_end():
            await asyncio.sleep(self.FPS)
            current_time = asyncio.get_event_loop().time()
            delta = current_time - last_update
            if delta >= self.FPS:
                # Pongを更新
                score_team: Optional[
                    str
                ] = await self.pong_logic.update_game_state()

                # consumerに送るメッセージを送信
                game_state = self._build_message(
                    match_constants.Stage.PLAY.value,
                    {
                        "paddle1_pos": {
                            "x": self.pong_logic.paddle1_pos.x,
                            "y": self.pong_logic.paddle1_pos.y,
                        },
                        "paddle2_pos": {
                            "x": self.pong_logic.paddle2_pos.x,
                            "y": self.pong_logic.paddle2_pos.y,
                        },
                        "ball": {
                            "x": self.pong_logic.ball_pos.x,
                            "y": self.pong_logic.ball_pos.y,
                        },
                        "score1": self.pong_logic.score1,
                        "score2": self.pong_logic.score2,
                    },
                )
                await self._send_message(game_state)

                # スコアの変動を確認
                if (
                    score_team is not None
                    and self.mode == match_constants.Mode.REMOTE.value
                ):
                    # TODO: スコアテーブルをバックグラウンドで作成。
                    pass

                last_update = current_time
            else:
                await asyncio.sleep(self.FPS - delta)

    async def _paddle_up(self, team: str) -> None:
        """
        PongLogicのパドル上に動かす操作関数

        Args:
            team (str): "1" | "2" チーム名
        """
        await self.pong_logic.move_paddle_up(team)

    async def _paddle_down(self, team: str) -> None:
        """
        PongLogicのパドル下に動かす操作関数

        Args:
            team (str): "1" | "2" チーム名
        """
        await self.pong_logic.move_paddle_down(team)

    async def _end_game(self) -> None:
        """
        試合の終了処理を行う関数
        """
        # 参加プレーヤーが退出したら、send_taskが終了していないかのうせいがあるので、終了させる。
        if self.send_task:
            self.send_task.cancel()

        # TODO: MatchのステータスをCOMPLETEDに更新

        # ゲーム終了後、Consumerに終了通知
        win_team = self.pong_logic.get_winner()
        message = self._build_message(
            match_constants.Stage.END.value,
            {
                "win": win_team,
                "score1": self.pong_logic.score1,
                "score2": self.pong_logic.score2,
            },
        )
        await self._send_message(message)

    async def player_exited(self, exited_team: str) -> None:
        """
        プレーヤーが途中退出した場合にConsumerから実行される関数。
        残っているプレーヤーを勝者にし、メッセージを送信。
        レコードの更新を行う。
        """
        # 参加プレーヤーが退出したら、バックグラウンドタスクが終了していない可能性があるので、終了させる。
        if self.wait_message:
            self.wait_message.cancel()
        if self.send_task:
            self.send_task.cancel()

        # TODO: 勝ったプレーヤーのレコードを更新。
        # TODO: MatchのステータスをCANCELEDに更新
        message = self._build_message(
            match_constants.Stage.END.value,
            {
                "win": match_constants.Team.ONE.value
                if exited_team != match_constants.Team.ONE.value
                else match_constants.Team.TWO.value,
                "score1": self.pong_logic.score1,
                "score2": self.pong_logic.score2,
            },
        )
        await self._send_message(message)

    def _build_message(self, stage: str, data: dict) -> dict:
        """
        プレーヤーに送るメッセージを作成。

        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.MATCH.value,
            ws_constants.PAYLOAD_KEY: {
                match_constants.Stage.key(): stage,
                ws_constants.DATA_KEY: data,
            },
        }

    async def _send_message(self, message: dict) -> None:
        """
        ローカル対戦であれば、Consumerへ送信
        リモート対戦であれば、グループへ送信
        """
        if self.mode == match_constants.Mode.LOCAL.value:
            await self.channel_handler.send_to_consumer(
                message, self.player1.channel_name
            )
        else:
            await self.channel_handler.send_to_group(self.group_name, message)
