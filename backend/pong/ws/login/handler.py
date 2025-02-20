from typing import Optional

from channels.layers import BaseChannelLayer  # type: ignore
from django.contrib.auth.models import User
from rest_framework import serializers

from users.friends import models as friend_models
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

        Exceptions:
            ValidationError: user_idが有効でなかった場合
            KeyError: user_idがint出なかった場合
        """
        # すでにログイン済みであれば無視
        if self.user_id:
            return

        self.user_id = payload[login_constants.USER_ID]

        # バリデーション失敗したら例外を投げる
        await self._validate_user_id()
        await self._login()

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
        await self._send_login_result(login_constants.Status.OK.value)
        # TODO: followerに通知する処理をmessageルールが決まったら追加

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
        # TODO: followerに通知する処理をmessageルールが決まったら追加

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
            await self._send_login_result(login_constants.Status.ERROR.value)
            raise serializers.ValidationError(
                f"Invalid user_id: {self.user_id}"
            )

    async def _send_login_result(self, login_status: str) -> None:
        message = {
            ws_constants.Category.key(): ws_constants.Category.LOGIN,
            ws_constants.PAYLOAD_KEY: {login_constants.Status: login_status},
        }
        await self.channel_handler.send_to_consumer(
            message, self.channel_handler.channel_name
        )

    # TODO: ログインかログアウトかを引数で受け取る
    async def _notify_followers(self) -> None:
        # TODO: 決定したmessageに変更
        message = {
            ws_constants.Category.key(): ws_constants.Category.LOGIN,
            ws_constants.PAYLOAD_KEY: {login_constants.USER_ID: self.user_id},
        }
        # オンライン状態でフレンド登録している人をイテレーションで順に処理
        async for follower_id in (
            friend_models.Friendship.objects.filter(friend_id=self.user_id)
            .values_list("id", flat=True)
            .aiterator()
        ):
            # followerのうちがオンライン状態であるユーザーのchannel名の集合を取得
            channel_set: set[str] = await AsyncRedisClient.smembers_value(
                login_constants.USER_NAMESPACE,
                follower_id,
                login_constants.CHANNEL_RESOURCE,
            )

            # onlineのフォロワーのchannelすべてに送信
            for channel in channel_set:
                await self.channel_handler.send_to_consumer(message, channel)
