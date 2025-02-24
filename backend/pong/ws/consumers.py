import logging

from channels.generic.websocket import (  # type: ignore
    AsyncJsonWebsocketConsumer,
)
from rest_framework import serializers

from .match import handler as match_handler
from .share import constants as ws_constants
from .share import serializers as ws_serializers

logger = logging.getLogger(__name__)


class MultiEventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self) -> None:
        # TODO:login用のハンドラが作成したら追加
        # match用のハンドラを作成
        self.match_handler = match_handler.MatchHandler(
            self.channel_layer, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.match_handler.cleanup()

    async def receive_json(self, message: dict) -> None:
        try:
            serializer = ws_serializers.WebsocketInputSerializer(data=message)
            serializer.is_valid(raise_exception=True)

            category: str = serializer.validated_data[
                ws_constants.Category.key()
            ]
            payload: dict = serializer.validated_data[ws_constants.PAYLOAD_KEY]

            # TODO: LOGINメッセージルール確定したら追加
            match category:
                case ws_constants.Category.MATCH.value:
                    await self.match_handler.handle(payload)
                case _:
                    logger.warning(f"Unknown category received: {category}")

        except serializers.ValidationError as e:
            # バリデーションエラーの時のエラーハンドリング
            logger.warning(f"Invalid schema: {str(e)}, message: {message}")
        except Exception as e:
            # サーバー側の予期しないエラーが起きても切断したくないのでここで拾い、ログレベルerrorで出力する
            logger.error(
                f"Unexpected server error occurred: {str(e)}, message: {message}"
            )

    async def group_message(self, event: dict) -> None:
        message = event["message"]
        await self.send_json(message)
