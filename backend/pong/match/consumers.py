from channels.generic.websocket import (  # type: ignore
    AsyncJsonWebsocketConsumer,
)

from . import match_handler


class MultiEventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self) -> None:
        # match用のハンドラを作成
        self.match_handler = match_handler.MatchHandler(
            self.channel_layer, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        pass

    async def receive_json(self, message: dict) -> None:
        category: str = message.get("category", "")
        payload: dict = message.get("payload", {})

        match category:
            case "MATCH":
                await self.match_handler.handle(payload)
            case _:
                pass

    async def group_message(self, event: dict) -> None:
        message = event["message"]
        await self.send_json(message)
