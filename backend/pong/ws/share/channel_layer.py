from channels.layers import BaseChannelLayer  # type: ignore


class ChannelLayer:
    """
    グループ関係のメソッド
    """

    @staticmethod
    async def add_to_group(
        channel_layer: BaseChannelLayer, group_name: str, channel_name: str
    ) -> None:
        """
        Consumerをグループに追加。

        チャネル名を指定したグループに登録する。
        """
        await channel_layer.group_add(group_name, channel_name)

    @staticmethod
    async def remove_from_group(
        channel_layer: BaseChannelLayer, group_name: str, channel_name: str
    ) -> None:
        """
        Consuerをグループから削除。

        チャネル名を指定したグループから退出させる。
        """
        await channel_layer.group_discard(group_name, channel_name)

    @staticmethod
    async def send_to_group(
        channel_layer: BaseChannelLayer, group_name: str, message: dict
    ) -> None:
        """
        グループにメッセージを送信。

        :param message: 送信するメッセージ
        """
        await channel_layer.group_send(
            group_name, {"type": "group.message", "message": message}
        )
