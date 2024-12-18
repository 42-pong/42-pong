from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import match_handler


class MultiEventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # match用のハンドラを作成
        self.match_handler = match_handler.MatchHandler(
            self.channel_layer, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, message):
        category = message.get("category")
        payload = message.get("payload")

        match category:
            case "MATCH":
                await self.match_handler.handle(payload)
            case _:
                pass

    async def group_message(self, event):
        message = event["message"]
        await self.send_json(message)
