from channels.layers import BaseChannelLayer  # type: ignore

from ..share import channel_handler


class LoginHandler:
    """
    クライアントのログインに関するハンドリングをするクラス
    """

    def __init__(self, channel_layer: BaseChannelLayer, channel_name: str):
        self.channel_handler = channel_handler.ChannelHandler(
            channel_layer, channel_name
        )

    def __str__(self) -> str:
        return "LoginHandler"

    def __repr__(self) -> str:
        return f"LoginHandler(" f"channel_handler={self.channel_handler!r})"

    async def handle(self, payload: dict) -> None:
        """
        クライアントからの入力を受け取り、正しい入力であればログインとして扱うためのハンドラ関数
        """
        pass

    async def _login() -> None:
        """
        redisにlogin情報を登録
        """
        pass

    async def logout() -> None:
        """
        redisからlogin情報を削除
        websocket切断時に呼び出される
        """
        pass

    async def validate_user_id(self, user_id):
        """
        messageで受け取ったuser_idが有効かどうかバリデーションを行う
        """
        pass
