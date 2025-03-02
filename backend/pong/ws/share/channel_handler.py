from typing import Optional

from channels.layers import BaseChannelLayer  # type: ignore


class ChannelHandler:
    """
    グループ関係のメソッド
    """

    def __init__(
        self, channel_layer: BaseChannelLayer, channel_name: Optional[str]
    ) -> None:
        self.channel_layer = channel_layer
        self.channel_name = channel_name

    def __str__(self) -> str:
        """
        読みやすい文字列表現を返す。
        """
        return f"ChannelHandler(channel_layer={self.channel_layer}, channel_name={self.channel_name})"

    def __repr__(self) -> str:
        """
        デバッグ用の公式な文字列表現を返す。
        """
        return f"ChannelHandler(channel_layer={self.channel_layer!r}, channel_name={self.channel_name!r})"

    async def add_to_group(
        self, group_name: str, channel_name: Optional[str] = None
    ) -> None:
        """
        Consumerをグループに追加。

        チャネル名を指定したグループに登録する。

        :param group_name: 追加するグループ名
        """
        if channel_name is None:
            channel_name = self.channel_name
        if channel_name is not None:
            await self.channel_layer.group_add(group_name, channel_name)

    async def remove_from_group(
        self, group_name: str, channel_name: Optional[str] = None
    ) -> None:
        """
        Consumerをグループから削除。

        チャネル名を指定したグループから退出させる。

        :param group_name: 削除するグループ名
        """
        if channel_name is None:
            channel_name = self.channel_name
        if channel_name is not None:
            await self.channel_layer.group_discard(group_name, channel_name)

    async def send_to_group(self, group_name: str, message: dict) -> None:
        """
        グループにメッセージを送信。

        :param group_name: メッセージを送信するグループ名
        :param message: 送信するメッセージ
        """
        await self.channel_layer.group_send(
            group_name, {"type": "group.message", "message": message}
        )

    async def send_to_consumer(self, message: dict, channel_name: str) -> None:
        """
        接続されている個々のConsumer（クライアント）にメッセージを送信。

        :param message: 送信するメッセージ
        """
        await self.channel_layer.send(
            channel_name, {"type": "websocket.send", "text": message}
        )
