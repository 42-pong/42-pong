import logging

from django.db.models import Q
from rest_framework import (
    exceptions,
    permissions,
    response,
    status,
    viewsets,
)

from pong.custom_response import custom_response
from users import constants as users_constants

from . import models

logger = logging.getLogger(__name__)


class BlocksViewSet(viewsets.ViewSet):
    queryset = models.BlockRelationship.objects.filter(
        Q(blocked_user__player__isnull=False)
    ).select_related("user", "blocked_user")
    permission_classes = (permissions.IsAuthenticated,)

    def handle_exception(self, exc: Exception) -> response.Response:
        """
        ModelViewSetのhandle_exception()をオーバーライド
        viewでtry-exceptしていない例外をカスタムレスポンスに変換して返す
        """
        if isinstance(
            exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)
        ):
            logger.error(f"[401] Authentication error: {str(exc)}")
            # 401はCustomResponseにせずそのまま返す
            return super().handle_exception(exc)

        logger.error(f"[500] Internal server error: {str(exc)}")
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse(
                code=[users_constants.Code.INTERNAL_ERROR],
                errors={"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )
        return response
