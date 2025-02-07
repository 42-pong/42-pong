from channels.layers import BaseChannelLayer  # type: ignore

from ..share import channel_handler
from ..share import constants as ws_constants
from . import constants as tournament_constants


class TournamentHandler:
    """
    トーナメントイベントのハンドラークラス
    主に以下の役割を果たす
        - Tournamentイベントのメッセージの処理と送信
        - ChannelLayerのグループ参加・退出を管理
        - Redisを通して、Tournament進行管理インスタンスとやり取り
    """

    def __init__(self, channel_layer: BaseChannelLayer, channel_name: str):
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

    async def handle(self, payload: dict) -> None:
        """
        consumerから呼ばれる、payloadごとに処理を振り分ける関数
        """
        type: str = payload[tournament_constants.Type.key()]
        data: dict = payload[ws_constants.DATA_KEY]
        handler = self.type_handlers[type]

        if callable(handler):
            await handler(data)

    async def _handle_join(self, data: dict) -> None:
        """
        playerがtournamentに参加する際の処理を行う関数
        """
        join_type: str = data[tournament_constants.Type.key()]
        match join_type:
            case tournament_constants.JoinType.CREATE.value:
                # TODO: TournamentManager作成
                # TODO: Redisに参加登録
                pass

            case tournament_constants.JoinType.RANDOM.value:
                # TODO: ランダムな募集中のトーナメントをフェッチ
                # TODO: Redisに参加登録
                pass

            case tournament_constants.JoinType.SELECTED.value:
                # TODO: Redisに参加PUBLISH
                # TODO: DBに参加レコード作成
                pass

            case _:
                pass

        await self._reload_player_change()  # 全員にPLAYER情報のRELOAD通知

    async def _handle_leave(self, data: dict) -> None:
        """
        playerからtournamentから退出する際の処理を行う関数
        """
        # TODO: Redisに退出PUBLISH
        # TODO: 参加レコード削除のDBアクセス
        await self._reload_player_change()  # 全員にPLAYER情報のRELOAD通知

    async def _reload_player_change(self) -> None:
        """
        参加者情報をフェッチするようグループに通知
        """
        pass

    async def _reload_tournament_state_change(self) -> None:
        """
        トーナメント状態をフェッチするようグループに通知
        """
        pass
