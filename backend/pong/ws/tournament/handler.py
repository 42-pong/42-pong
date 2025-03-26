import logging
from typing import Optional

from channels.layers import BaseChannelLayer  # type: ignore

from tournaments import constants as tournament_db_constants

from ..share import channel_handler, player_data
from ..share import constants as ws_constants
from . import async_db_service as db_service
from . import constants as tournament_constants
from . import manager_registry

logger = logging.getLogger(__name__)


class TournamentHandler:
    """
    トーナメントイベントのハンドラークラス
    主に以下の役割を果たす
        - Tournamentイベントのメッセージの処理と送信
        - ChannelLayerのグループ参加・退出を管理
        - Redisを通して、Tournament進行管理インスタンスとやり取り
    """

    def __init__(
        self,
        channel_layer: BaseChannelLayer,
        channel_name: str,
    ):
        """
        TournamentHandlerの初期化。

        :param channel_layer: チャネルレイヤー
        :param channel_name: チャネル名
        """
        self.type_handlers = {
            tournament_constants.Type.JOIN.value: self._handle_join,
            tournament_constants.Type.LEAVE.value: self._handle_leave,
        }
        self.channel_handler: channel_handler.ChannelHandler = (
            channel_handler.ChannelHandler(channel_layer, channel_name)
        )
        self.manager_registry = manager_registry.global_tournament_registry
        self.user_id: Optional[int] = None
        self.tournament_id: Optional[int] = None
        self.player_data: Optional[player_data.PlayerData] = None

    def __str__(self) -> str:
        """
        TournamentHandlerオブジェクトを文字列として表現したものを返す。
        """
        return f"TournamentHandler(channel_name={self.channel_handler})"

    def __repr__(self) -> str:
        """
        デバッグ用途でTournamentHandlerオブジェクトの詳細な表現の文字列を返す。
        """
        return f"TournamentHandler(channel_handler={self.channel_handler!r})"

    async def handle(self, payload: dict, user_id: Optional[int]) -> None:
        """
        consumerから呼ばれる、payloadごとに処理を振り分ける関数
        """
        # まだログインしていないユーザーからのメッセージは無視
        if user_id is None:
            return
        # まだログインしてから初回のメッセージでuser_idを登録
        if self.user_id is None:
            self.user_id = user_id

        type: str = payload[tournament_constants.Type.key()]
        data: dict = payload[ws_constants.DATA_KEY]
        handler = self.type_handlers[type]

        if callable(handler):
            await handler(data)

    async def _handle_join(self, data: dict) -> None:
        """
        playerがtournamentに参加する際の処理を行う関数
        """
        join_type: str = data[tournament_constants.JOIN_TYPE]
        participation_name: Optional[str] = data[
            tournament_constants.PARTICIPATION_NAME
        ]
        # participation_nameは参加に必須。
        if participation_name is None:
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        # 参加データを更新。
        self.player_data = self._create_player_data(participation_name)

        # JOINタイプによってハンドラを呼び分ける
        if join_type == tournament_constants.JoinType.CREATE.value:
            await self._handle_create_join(participation_name)
        elif join_type == tournament_constants.JoinType.RANDOM.value:
            await self._handle_random_join()
        elif join_type == tournament_constants.JoinType.SELECTED.value:
            await self._handle_selected_join(data)

    async def _handle_create_join(self, participation_name: str) -> None:
        """
        トーナメント作成し参加した場合のハンドラ
        """
        # 型チェック用
        if self.player_data is None:
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        result = await db_service.create_tournament_with_participation(
            self.user_id, participation_name
        )
        if result.is_error:
            logger.error(f"Error: {result.unwrap_error()}")
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        tournament_id = result.unwrap()[
            tournament_db_constants.TournamentFields.ID
        ]
        # 参加するトーナメントIDをセット
        self.tournament_id = tournament_id

        await self.manager_registry.create_tournament(
            tournament_id, self.player_data
        )
        await self.channel_handler.add_to_group(f"tournament_{tournament_id}")
        await self._send_join_result(
            tournament_constants.Status.OK.value, tournament_id
        )

    async def _handle_random_join(self) -> None:
        """
        ランダムなトーナメントに参加した場合のハンドラ
        """
        # 型チェック用
        if self.player_data is None:
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        tournament_id = await db_service.get_waiting_tournament()
        if tournament_id is None:
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        success = await self.manager_registry.add_participant(
            tournament_id, self.player_data
        )
        if success:
            # 参加するトーナメントIDをセット
            self.tournament_id = tournament_id
        status = (
            tournament_constants.Status.OK.value
            if success
            else tournament_constants.Status.ERROR.value
        )
        await self._send_join_result(status, tournament_id)

    async def _handle_selected_join(self, data: dict) -> None:
        """
        tournament_idを指定して参加した場合のハンドラ
        """
        # 型チェック用
        if self.player_data is None:
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        tournament_id = data.get(tournament_constants.TOURNAMENT_ID)
        if tournament_id is None:
            await self._send_join_result(
                tournament_constants.Status.ERROR.value, None
            )
            return

        success = await self.manager_registry.add_participant(
            tournament_id, self.player_data
        )
        if success:
            # 参加するトーナメントIDをセット
            self.tournament_id = tournament_id
        status = (
            tournament_constants.Status.OK.value
            if success
            else tournament_constants.Status.ERROR.value
        )
        await self._send_join_result(status, tournament_id)

    async def _handle_leave(self, data: dict) -> None:
        """
        playerからtournamentから退出する際の処理を行う関数
        """
        tournament_id = data[tournament_constants.TOURNAMENT_ID]
        if tournament_id is None:  # IDが数値でない場合はエラー
            return

        if self.player_data is None:
            return

        await self.manager_registry.remove_participant(
            tournament_id, self.player_data
        )

        # 退出したので、トーナメントIDを削除
        self.tournament_id = None

    def _create_player_data(
        self, participation_name: Optional[str]
    ) -> Optional[player_data.PlayerData]:
        """
        プレーヤーデータを作成する関数
        """
        channel_name = self.channel_handler.channel_name
        if self.user_id is None or channel_name is None:
            return None

        return player_data.PlayerData(
            channel_name=channel_name,
            user_id=self.user_id,
            participation_name=participation_name,
        )

    async def _send_join_result(
        self, status: str, tournament_id: Optional[int]
    ) -> None:
        """
        JOINメッセージの結果を通知する関数
        """
        message = self._build_tournament_message(
            tournament_constants.Type.JOIN.value,
            {
                tournament_constants.Status.key(): status,
                tournament_constants.TOURNAMENT_ID: tournament_id,
            },
        )
        if self.channel_handler.channel_name is not None:
            await self.channel_handler.send_to_consumer(
                message, self.channel_handler.channel_name
            )

    def _build_tournament_message(self, type: str, data: dict) -> dict:
        """
        プレーヤーに送るメッセージを作成。

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

    async def exit(self) -> None:
        """
        トーナメントに参加中に切断した場合、トーナメント進行クラスに退出を伝えるための関数
        """
        # loginしていないか、トーナメント参加中でなければ特に何もしない
        if self.player_data is None or self.tournament_id is None:
            return

        await self.manager_registry.remove_participant(
            self.tournament_id, self.player_data
        )
