import logging
from typing import Any, Optional

from channels.layers import BaseChannelLayer  # type: ignore
from django.contrib.auth.models import User
from rest_framework import serializers

from ws.share.async_redis_client import AsyncRedisClient  # type: ignore

from ..login import constants as login_constants
from ..share import channel_handler
from ..share import constants as ws_constants
from ..tournament import manager_registry as tournament_manager_registry
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
        from_user_id: Optional[Any] = payload.get(chat_constants.FROM)
        await self._validate_user_id(from_user_id)
        to_user_id: Optional[Any] = payload.get(chat_constants.TO)
        await self._validate_user_id(to_user_id)
        pass

    async def _handle_invite(self, payload: dict) -> None:
        # TODO: # 相手がオンラインなら送信する
        from_user_id: Optional[Any] = payload.get(chat_constants.FROM)
        await self._validate_user_id(from_user_id)
        to_user_id: Optional[Any] = payload.get(chat_constants.TO)
        await self._validate_user_id(to_user_id)
        pass

    async def _handle_group_chat(self, payload: dict) -> None:
        """
        グループチャット用のハンドラ関数
        TournamentManagerRegistryを通して、トーナメントグループに送る
        """
        from_user_id: Optional[Any] = payload.get(chat_constants.FROM)
        await self._validate_user_id(from_user_id)
        tournament_id = payload.get(chat_constants.TO)
        if tournament_id is None:
            return

        message = self._build_chat_message(
            chat_constants.Type.GROUP_CHAT.value, payload
        )
        await tournament_manager_registry.global_tournament_registry.send_group_chat(
            tournament_id, message
        )
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

    async def _is_online_user(self, user_id: int) -> bool:
        """
        引数で受け取ったuser_idのユーザーのオンライン状態を取得する関数
        """
        exist = await AsyncRedisClient.exists(
            login_constants.USER_NAMESPACE,
            user_id,
            login_constants.CHANNEL_RESOURCE,
        )
        return exist

    async def _validate_user_id(self, input_user_id: Optional[Any]) -> None:
        """
        messageで受け取ったuser_idが有効かどうかバリデーションを行う
        """
        exists = False
        # Noneなら呼ばれない想定だがtype checkのために確認
        if isinstance(input_user_id, int):
            # 非同期にUserを取得
            exists = await User.objects.filter(id=input_user_id).aexists()

        if not exists:
            raise serializers.ValidationError(
                f"Invalid user_id: {input_user_id}"
            )
