import logging

from channels.generic.websocket import (  # type: ignore
    AsyncJsonWebsocketConsumer,
)
from rest_framework import serializers

from .chat import handler as chat_handler
from .login import handler as login_handler
from .match import handler as match_handler
from .share import constants as ws_constants
from .share import serializers as ws_serializers
from .tournament import handler as tournament_handler

logger = logging.getLogger(__name__)


class MultiEventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self) -> None:
        # それぞれのイベントのハンドラを作成
        self.login_handler = login_handler.LoginHandler(
            self.channel_layer, self.channel_name
        )
        self.match_handler = match_handler.MatchHandler(self.channel_name)
        self.tournament_handler = tournament_handler.TournamentHandler(
            self.channel_layer,
            self.channel_name,
        )
        self.chat_handler = chat_handler.ChatHandler(
            self.channel_layer,
            self.channel_name,
        )

        await self.accept()
        logger.debug(f"accept: {self.channel_name}")

    async def disconnect(self, close_code: int) -> None:
        await self.login_handler.logout()
        await self.match_handler.cleanup()
        logger.debug(f"disconnect: {self.channel_name}")

    async def receive_json(self, message: dict) -> None:
        try:
            serializer = ws_serializers.WebsocketInputSerializer(data=message)
            serializer.is_valid(raise_exception=True)

            category: str = serializer.validated_data[
                ws_constants.Category.key()
            ]
            payload: dict = serializer.validated_data[ws_constants.PAYLOAD_KEY]

            match category:
                case (
                    ws_constants.Category.LOGIN.value
                    | ws_constants.Category.STATUS.value
                ):
                    await self.login_handler.handle(payload)
                case ws_constants.Category.MATCH.value:
                    await self.match_handler.handle(
                        payload, self.login_handler.user_id
                    )
                case ws_constants.Category.TOURNAMENT.value:
                    await self.tournament_handler.handle(
                        payload, self.login_handler.user_id
                    )
                case ws_constants.Category.CHAT.value:
                    await self.chat_handler.handle(
                        payload, self.login_handler.user_id
                    )
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

    async def websocket_send(self, event: dict) -> None:
        message = event.get("text", "")
        await self.send_json(message)
