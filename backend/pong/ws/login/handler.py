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
            KeyError: payload内のkeyが'user_id'ではなかった場合
        """
        if self.user_id is not None:
            # ログイン後は新規フレンド追加時にそのフレンドのオンライン状態を返す
            await self.handle_online_status(payload)
            return

        input_user_id: int = payload[login_constants.USER_ID]

        # バリデーション失敗したら例外を投げる
        await self._validate_user_id(input_user_id)
        await self._login(input_user_id)

    async def handle_online_status(self, payload: dict) -> None:
        """
        あるユーザーがオンラインかどうかを通知するハンドラー
        メッセージに入っているuser_idのユーザーがオンラインかどうか判定し、メッセージを返す。
        """
        input_user_id: int = payload[login_constants.USER_ID]

        # 存在しないユーザーであれば例外を投げる
        await self._validate_user_id(input_user_id)

        # もし自分のオンライン状態を確認しようとしていたら無視
        if input_user_id == self.user_id:
            return

        exist = await AsyncRedisClient.exists(
            login_constants.USER_NAMESPACE,
            input_user_id,
            login_constants.CHANNEL_RESOURCE,
        )
        message = self._build_a_user_online_status_message(
            input_user_id, exist
        )

        # 型ヒントで必要なチェック
        if self.channel_handler.channel_name is not None:
            await self.channel_handler.send_to_consumer(
                message, self.channel_handler.channel_name
            )

    async def _login(self, input_user_id: int) -> None:
        """
        redisにlogin情報を登録
        login結果とユーザーのフレンドのオンライン情報を送信
        """
        self.user_id = input_user_id
        connection_cnt = await AsyncRedisClient.sadd_value(
            login_constants.USER_NAMESPACE,
            self.user_id,
            login_constants.CHANNEL_RESOURCE,
            self.channel_handler.channel_name,
        )
        await self._send_login_result(login_constants.Status.OK.value)

        # 接続数が0->1の時だけfollowerに通知する
        if connection_cnt == 1:
            await self._notify_followers(True)

    async def logout(self) -> None:
        """
        redisからlogin情報を削除
        websocket切断時に呼び出される
        """
        connection_cnt = await AsyncRedisClient.srem_value(
            login_constants.USER_NAMESPACE,
            self.user_id,
            login_constants.CHANNEL_RESOURCE,
            self.channel_handler.channel_name,
        )
        self.user_id = None

        # 接続数が1->0の時だけfollowerに通知する
        if connection_cnt == 0:
            await self._notify_followers(False)

    async def _validate_user_id(self, input_user_id: int) -> None:
        """
        messageで受け取ったuser_idが有効かどうかバリデーションを行う
        """
        exists = False
        # Noneなら呼ばれない想定だがtype checkのために確認
        if isinstance(input_user_id, int):
            # 非同期にUserを取得
            exists = await User.objects.filter(id=input_user_id).aexists()

        if not exists:
            await self._send_login_result(login_constants.Status.ERROR.value)
            raise serializers.ValidationError(
                f"Invalid user_id: {input_user_id}"
            )

    async def _send_login_result(self, login_status: str) -> None:
        online_friend_list: list[int] = await self.get_friends_online_status()
        message = {
            ws_constants.Category.key(): ws_constants.Category.LOGIN.value,
            ws_constants.PAYLOAD_KEY: {
                login_constants.Status.key(): login_status,
                login_constants.ONLINE_FRIEND_IDS: online_friend_list,
            },
        }
        await self.channel_handler.send_to_consumer(
            message, self.channel_handler.channel_name
        )

    async def _notify_followers(self, is_login: bool) -> None:
        # 型チェックで必要なチェック
        if self.user_id is None:
            return

        message = self._build_a_user_online_status_message(
            self.user_id, is_login
        )

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

    async def get_friends_online_status(self) -> list[int]:
        """
        フレンドのオンライン情報を取得して、クライアントに送信する。
        Redis からオンラインのフレンドの情報を非同期で取得する。
        """
        # 型チェック的に必要
        if self.user_id is None:
            return []

        # オンラインのフレンドを格納するリスト
        online_friends = []

        # フレンドリストを取得 (非同期)
        async for friend_id in (
            friend_models.Friendship.objects.filter(user_id=self.user_id)
            .values_list("friend_id", flat=True)
            .aiterator()
        ):
            # 友達がオンラインかどうかをチェック (Redis から取得)
            exist = await AsyncRedisClient.exists(
                login_constants.USER_NAMESPACE,
                friend_id,
                login_constants.CHANNEL_RESOURCE,
            )

            # オンラインであればリストに追加
            if exist:
                online_friends.append(friend_id)

        return online_friends

    def _build_a_user_online_status_message(
        self, user_id: int, is_online: bool
    ) -> dict:
        message = {
            ws_constants.Category.key(): ws_constants.Category.STATUS.value,
            ws_constants.PAYLOAD_KEY: {
                login_constants.USER_ID: user_id,
                login_constants.ONLINE: is_online,
            },
        }
        return message
