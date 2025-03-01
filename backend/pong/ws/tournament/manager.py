import asyncio

from channels.layers import get_channel_layer  # type: ignore

from ws.share import constants as ws_constants

from ..share import channel_handler, player_data
from . import constants as tournament_constants


class TournamentManager:
    """
    4人のConsumerとやり取りをしながらトーナメント進行をするためのクラス

    4人と専用のチャネルレイヤーを持つためにユニークなグループ名を持つ。
    基本的にConsumerからは関数を通してアクションを受け取って、チャネルレイヤーを通してConsumerに通知する。

    group_name: 'tournament_{tournament_id}'
    """

    def __init__(self, tournament_id: int) -> None:
        self.tournament_id: int = tournament_id
        self.group_name: str = f"tournament_{self.tournament_id}"
        self.participants: list[
            player_data.PlayerData
        ] = []  # 参加者の情報のリスト
        self.channel_handler = channel_handler.ChannelHandler(
            get_channel_layer(), None
        )
        self.waiting_for_participants = (
            asyncio.Event()
        )  # 参加者を待機するイベント

    async def add_participant(
        self, participant: player_data.PlayerData
    ) -> None:
        """
        参加者を追加。DBにも参加テーブルを作成する。
        参加者が4人になったらトーナメントを開始する。
        """
        self.participants.append(participant)
        # TODO: 参加レコードを作成
        await self._send_player_reload_message()

        if len(self.participants) == 4:
            # 4人集まったらイベントをセットしてトーナメントを開始
            self.waiting_for_participants.set()

    async def remove_participant(
        self, participant: player_data.PlayerData
    ) -> None:
        """
        参加者を削除。DBから参加テーブルを削除する。
        """
        pass

    async def run(self) -> None:
        """
        トーナメントのすべての進行を管理する関数
        """
        # 4人参加するまで待機。
        await self.waiting_for_participants.wait()

        # トーナメントの開始処理を行う。
        await self._start_tournament()

        # ラウンドを1つずつ進める。
        # もし次のラウンドが残っていれば再び実行される。
        await self._progress_rounds()

        # トーナメントの終了処理を行う。
        await self._end_tournament()

    async def _start_tournament(self) -> None:
        """
        トーナメント開始処理。
        トーナメントの状態を変更し、Consumerへ通知する。
        リソースを作成した後に、ラウンドを作成する。
        """
        pass

    async def _progress_rounds(self) -> None:
        """
        ラウンド進行処理。
        participantを2人組にして、それぞれにマッチを作成。
        すべてのmatchが終わるのを待ち、まだ優勝者が決まらなければもう一度ラウンドを進行し、決まればトーナメントを終了する。
        """
        pass

    async def _end_tournament(self) -> None:
        """
        トーナメント終了処理。
        """
        pass

    async def cancel_tournament(self) -> None:
        """
        トーナメント中止処理。
        """
        pass

    async def _send_player_reload_message(self) -> None:
        """
        参加者が変わったことをConsumerに伝える関数
        これを受け取ったプレーヤーはRESTAPIで情報を取得し、画面を更新する。
        """
        message = self._build_tournament_message(
            tournament_constants.Type.RELOAD.value,
            {
                tournament_constants.Event.key(): tournament_constants.Event.PLAYER_CHANGE.value
            },
        )
        await self.channel_handler.send_to_group(self.group_name, message)

    async def _send_tournament_reload_message(self) -> None:
        """
        トーナメントの状態が変わったことをConsumerに伝える関数
        これを受け取ったプレーヤーはRESTAPIで情報を取得し、画面を更新する。
        """
        message = self._build_tournament_message(
            tournament_constants.Type.RELOAD.value,
            {
                tournament_constants.Event.key(): tournament_constants.Event.TOURNAMENT_STATE_CHANGE.value
            },
        )
        await self.channel_handler.send_to_group(self.group_name, message)

    def _build_tournament_message(self, type: str, data: dict) -> dict:
        """
        プレーヤーに送るトーナメントメッセージを作成。

        :param data: ステージに関連するデータ
        :return: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.TOURNAMENT.value,
            ws_constants.PAYLOAD_KEY: {
                tournament_constants.Type.key(): type,
                ws_constants.DATA_KEY: data,
            },
        }
