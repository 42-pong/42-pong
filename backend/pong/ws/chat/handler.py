import logging
from typing import Optional

from channels.layers import BaseChannelLayer  # type: ignore

from ..share import channel_handler
from ..share import constants as ws_constants
from . import constants as chat_constants

logger = logging.getLogger(__name__)


class ChatHandler:
    def __init__(
        self,
        channel_layer: BaseChannelLayer,
        channel_name: str,
    ):
        self.type_handlers = {
            chat_constants.Type.DM.value: self._handle_dm,
            chat_constants.Type.INVITE.value: self._handle_invite,
            chat_constants.Type.GROUP_CHAT.value: self._handle_group_chat,
        }
        self.channel_handler: channel_handler.ChannelHandler = (
            channel_handler.ChannelHandler(channel_layer, channel_name)
        )
        self.user_id: Optional[int] = None

    async def handle(self, payload: dict, user_id: Optional[int]) -> None:
        if user_id is None:
            return
        # まだログインしてから初回のメッセージでuser_idを登録
        if self.user_id is None:
            self.user_id = user_id

        type: str = payload[chat_constants.Type.key()]
        data: dict = payload[ws_constants.DATA_KEY]
        handler = self.type_handlers[type]

        if callable(handler):
            await handler(data)

    async def _handle_dm(self, payload: dict) -> None:
        # TODO: # 相手がオンラインなら送信する
        pass

    async def _handle_invite(self, payload: dict) -> None:
        # TODO: # 相手がオンラインなら送信する
        pass

    async def _handle_group_chat(self, payload: dict) -> None:
        # TODO: TournamentManagerRegistryを通して、全体に送る
        pass

    def _build_chat_message(self, type: str, data: dict) -> dict:
        """
        プレーヤーに送るチャットメッセージを作成。

        Args:
            type (str): メッセージタイプ
            data (dict): メッセージ

        Return:
            dict: 作成したメッセージ
        """
        return {
            ws_constants.Category.key(): ws_constants.Category.CHAT.value,
            ws_constants.PAYLOAD_KEY: {
                chat_constants.Type.key(): type,
                ws_constants.DATA_KEY: data,
            },
        }
