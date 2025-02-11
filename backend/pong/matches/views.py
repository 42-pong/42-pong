from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import viewsets, permissions, request, response, status, views

from pong.custom_response import custom_response

from . import constants
from .match import models as match_models
from .match import serializers


class MatchReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = match_models.Match.objects.all().prefetch_related(
        "match_participations__scores"
    )
    serializer_class = serializers.MatchSerializer
