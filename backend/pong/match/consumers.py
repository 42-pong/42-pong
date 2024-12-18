from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import match_handler

class MultiEventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # match用のハンドラを作成
        self.match_handler = match_handler.MatchHandler()

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, message):
        category = message.get("category")
        payload = message.get("payload")

        match category:
            case "MATCH":
                # ここでマッチハンドラに処理移譲
                pass
            case _:
                pass
