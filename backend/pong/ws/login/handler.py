from typing import Optional

from channels.layers import BaseChannelLayer  # type: ignore
from django.contrib.auth.models import User
from rest_framework import serializers

from ws.share.async_redis_client import AsyncRedisClient  # type: ignore

from ..share import channel_handler
from ..share import constants as ws_constants
from . import constants as login_constants


class LoginHandler:
    """
    クライアントのログインに関するハンドリングをするクラス
    """

    def __init__(self, channel_layer: BaseChannelLayer, channel_name: str):
        self.channel_handler = channel_handler.ChannelHandler(
            channel_layer, channel_name
        )
        self.user_id: Optional[int] = None

    def __str__(self) -> str:
        return "LoginHandler"

    def __repr__(self) -> str:
        return f"LoginHandler(" f"channel_handler={self.channel_handler!r})"

    async def handle(self, payload: dict) -> None:
        """
        クライアントからの入力を受け取り、正しい入力であればログインとして扱うためのハンドラ関数
        """
        self.user_id = payload[login_constants.USER_ID]

    async def _login(self) -> None:
        """
        redisにlogin情報を登録
        """
        await AsyncRedisClient.sadd_value(
            login_constants.USER_NAMESPACE,
            self.user_id,
            login_constants.CHANNEL_RESOURCE,
            self.channel_handler.channel_name,
        )

    async def logout(self) -> None:
        """
        redisからlogin情報を削除
        websocket切断時に呼び出される
        """
        await AsyncRedisClient.srem_value(
            login_constants.USER_NAMESPACE,
            self.user_id,
            login_constants.CHANNEL_RESOURCE,
            self.channel_handler.channel_name,
        )

    async def _validate_user_id(self) -> None:
        """
        messageで受け取ったuser_idが有効かどうかバリデーションを行う
        """
        exists = None
        # Noneなら呼ばれない想定だがtype checkのために確認
        if isinstance(self.user_id, int):
            # 非同期にUserを取得
            exists = await User.objects.filter(id=self.user_id).aexists()

        if not exists:
            self.user_id = None
            raise serializers.ValidationError(
                f"Invalid user_id: {self.user_id}"
            )
