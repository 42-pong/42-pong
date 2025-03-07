import asyncio
import logging
from typing import Final, Optional

from channels.layers import get_channel_layer  # type: ignore

from matches import constants as match_db_constants
from ws.tournament import manager_registry as tournament_manager_registry

from ..share import channel_handler, player_data
from ..share import constants as ws_constants
from . import async_db_service as match_service
from . import constants as match_constants
from .pong_logic import PongLogic

logger = logging.getLogger(__name__)


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
        player2: Optional[player_data.PlayerData],
        mode: str,
        tournament_id: Optional[int] = None,
    ) -> None:
        """
        Args:
            match_id (int): matchのid
            player1 (PlayerData): player1の情報
            player2 (Optional[PlayerData]): player2の情報、ローカルならNone
            mode (str): "local" | "remote"のどちらか
        """
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.mode = mode

        self.pong_logic = PongLogic()
        self.group_name = f"pong_{match_id}"  # 一意
        self.ready_players = 0
        self.waiting_player_ready = asyncio.Event()
        self.canceled = False
        self.remained_player: Optional[player_data.PlayerData] = None
        self.channel_handler = channel_handler.ChannelHandler(
            get_channel_layer(), None
        )
        self.waiting_player_num = (
            1 if self.mode == match_constants.Mode.LOCAL.value else 2
        )
        self.tournament_id = tournament_id

    async def run(self) -> Optional[player_data.PlayerData]:
        """
        この関数を実行することでマッチを実行する。
        このクラスの作成側の関数はこの関数をバックグラウンドタスクとして実行し、終了を待つ。

        Returns:
            PlayerData:
                - 試合がキャンセルされた場合： 残ったプレーヤ―のデータを勝利者として返す。
                - 正常に終了した場合： 勝利プレーヤ―のデータを返す。
        """
        # プレーヤーが準備完了のメッセージを送信するのを待つ
        await self.waiting_player_ready.wait()

        if self.canceled:
            # 残っている方のPlayerDataを勝者として返す。
            return self.remained_player

        # PongLogic開始
        await self._start_game()

        if self.canceled:
            # 残っている方のPlayerDataを勝者として返す。
            return self.remained_player

        # ゲームが終了したら、Consumerに終了通知を送る
        await self._end_game()

        # 勝者チームのデータを返り値として返す。
        win_team = await self.pong_logic.get_winner()
        return (
            self.player1
            if win_team == match_constants.Team.ONE.value
            else self.player2
        )

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
        team = None
        if is_remote:
            team = (
                match_constants.Team.ONE.value
                if player.channel_name == self.player1.channel_name
                else match_constants.Team.TWO.value
            )
            await self.channel_handler.add_to_group(
                self.group_name, player.channel_name
            )

        message = self._build_message(
            match_constants.Stage.INIT.value,
            {
                match_constants.Team.key(): team,
                "display_name1": self.player1.participation_name
                if is_remote and self.player1 is not None
                else None,
                "display_name2": self.player2.participation_name
                if is_remote and self.player2 is not None
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

        # 全員からREADYメッセージが届いたらイベントをセットしてゲームを開始する。
        if self.ready_players == self.waiting_player_num:
            await self._send_message(message)
            self.waiting_player_ready.set()

    async def _start_game(self) -> None:
        """
        PongLogicの実行を開始し、ゲーム情報を送り続ける関数をバックグラウンドで実行する。
        """
        # MatchのステータスをON_GOINGに更新
        if self.mode == match_constants.Mode.REMOTE.value:
            update_result = await match_service.update_match_status(
                self.match_id,
                match_db_constants.MatchFields.StatusEnum.ON_GOING.value,
            )
            if update_result.is_error:
                logger.error(f"Error: {update_result.unwrap_error()}")

        # PongLogicの実行を開始
        self.send_task = asyncio.create_task(self._send_match_state())
        try:
            # send_taskが終わるまで待機
            await self.send_task
        except asyncio.CancelledError:
            # self.player_exited()でタスクがキャンセルされる例外をキャッチ
            return

    async def _send_match_state(self) -> None:
        """
        60FPSでPongLogicの状態を更新・取得し、Consumerに送信
        """
        last_update = asyncio.get_event_loop().time()
        while not await self.pong_logic.game_end():
            await asyncio.sleep(self.FPS)
            current_time = asyncio.get_event_loop().time()
            delta = current_time - last_update
            if delta >= self.FPS:
                # Pongを更新する前のボールの位置を保存
                pos_x, pos_y = (
                    self.pong_logic.ball_pos.x,
                    self.pong_logic.ball_pos.y,
                )
                # Pongを更新
                score_team: Optional[
                    str
                ] = await self.pong_logic.update_game_state()

                # consumerに送るメッセージを送信
                game_state = self._build_message(
                    match_constants.Stage.PLAY.value,
                    {
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
                        "score1": self.pong_logic.score1,
                        "score2": self.pong_logic.score2,
                    },
                )
                await self._send_message(game_state)

                # スコアの変動を確認
                if (
                    score_team is not None
                    and self.mode == match_constants.Mode.REMOTE.value
                    and self.player1 is not None
                    and self.player2 is not None
                ):
                    # スコアテーブルをバックグラウンドで作成。
                    scoring_player_id = (
                        self.player1.user_id
                        if score_team == match_constants.Team.ONE.value
                        else self.player2.user_id
                    )
                    asyncio.create_task(
                        match_service.create_score(
                            self.match_id, scoring_player_id, pos_x, pos_y
                        )
                    )
                    if self.tournament_id is not None:
                        asyncio.create_task(
                            tournament_manager_registry.global_tournament_registry.send_match_reload_message(
                                self.tournament_id
                            )
                        )

                last_update = current_time
            else:
                await asyncio.sleep(self.FPS - delta)

    async def paddle_up(self, team: str) -> None:
        """
        PongLogicのパドル上に動かす操作関数

        Args:
            team (str): "1" | "2" チーム名
        """
        await self.pong_logic.move_paddle_up(team)

    async def paddle_down(self, team: str) -> None:
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

        if self.send_task and not self.send_task.done():
            try:
                await self.send_task
            except asyncio.CancelledError:
                pass
        # 勝者チームを取得
        win_team = await self.pong_logic.get_winner()
        win_player = (
            self.player1
            if win_team == match_constants.Team.ONE.value
            else self.player2
        )

        # MatchのステータスをCOMPLETEDに更新
        if self.mode == match_constants.Mode.REMOTE.value:
            # 勝ったプレーヤーのレコードを更新
            if win_player is not None and win_player.user_id is not None:
                update_player_result = (
                    await match_service.update_participation_is_win(
                        self.match_id, win_player.user_id
                    )
                )
                if update_player_result.is_error:
                    logger.error(
                        f"Error: {update_player_result.unwrap_error()}"
                    )

            update_result = await match_service.update_match_status(
                self.match_id,
                match_db_constants.MatchFields.StatusEnum.COMPLETED.value,
            )
            if update_result.is_error:
                logger.error(f"Error: {update_result.unwrap_error()}")

        # ゲーム終了後、Consumerに終了通知
        message = self._build_message(
            match_constants.Stage.END.value,
            {
                "win": win_team,
                "score1": self.pong_logic.score1,
                "score2": self.pong_logic.score2,
            },
        )
        await self._send_message(message)

    async def player_exited(
        self, exited_player: player_data.PlayerData
    ) -> None:
        """
        プレーヤーが途中退出した場合にConsumerから実行される関数。
        呼び出されるタイミングは2つある。
        1. 試合開始前に退出した場合
        2. 試合中に退出した場合
            - どちらの場合も残っているプレーヤーを勝者にし、メッセージを送信。
            - レコードの更新を行う。
        """
        # run()関数内で認識できるようにキャンセルフラグを立てる
        self.canceled = True
        # 退出したほうのプレーヤーをNoneに変更
        self.remained_player = (
            self.player2 if exited_player == self.player1 else self.player1
        )

        if not self.waiting_player_ready.is_set():
            # 試合開始前に終了
            # もう必要ないのでREADYメッセージ待ちイベントをセット
            self.waiting_player_ready.set()
        else:
            # 試合中に退出した場合は、バックグラウンドタスクが終了していない可能性があるので、終了させる。
            if self.send_task:
                self.send_task.cancel()
                # キャンセルされるのを待つ
                await self.send_task

        # 残ったプレーヤーを勝者とする。
        if self.mode == match_constants.Mode.REMOTE.value:
            # 残ったプレーヤーのレコードを更新
            if (
                self.remained_player is not None
                and self.remained_player.user_id is not None
            ):
                update_player_result = (
                    await match_service.update_participation_is_win(
                        self.match_id, self.remained_player.user_id
                    )
                )
                if update_player_result.is_error:
                    logger.error(
                        f"Error: {update_player_result.unwrap_error()}"
                    )

            # MatchのステータスをCANCELEDに更新
            update_result = await match_service.update_match_status(
                self.match_id,
                match_db_constants.MatchFields.StatusEnum.CANCELED.value,
            )
            if update_result.is_error:
                logger.error(f"Error: {update_result.unwrap_error()}")

        # 試合結果を送信
        message = self._build_message(
            match_constants.Stage.END.value,
            {
                "win": match_constants.Team.ONE.value
                if exited_player == self.player2
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
