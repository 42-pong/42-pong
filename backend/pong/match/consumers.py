import logging

from channels.generic.websocket import (  # type: ignore
    AsyncJsonWebsocketConsumer,
)

from . import match_handler, ws_constants

logger = logging.getLogger("django")


class MultiEventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self) -> None:
        # match用のハンドラを作成
        self.match_handler = match_handler.MatchHandler(
            self.channel_layer, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.match_handler.cleanup()

    async def receive_json(self, message: dict) -> None:
        try:
            category: str = message[ws_constants.Category.key()]
            payload: dict = message[ws_constants.PAYLOAD_KEY]

            match category:
                case ws_constants.Category.MATCH.value:
                    await self.match_handler.handle(payload)
                case _:
                    logger.warning(f"Unknown category received: {category}")

        except Exception as e:
            # サーバー側の予期しないエラーが起きても切断したくないのでここで拾い、ログレベルerrorで出力する
            logger.error(
                f"Unexpected server error occurred: {str(e)}, message: {message}"
            )

    async def group_message(self, event: dict) -> None:
        message = event["message"]
        await self.send_json(message)
