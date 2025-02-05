from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from accounts import constants
from accounts.player import models
from pong.custom_response import custom_response

from .. import serializers


class UsersRetrieveView(views.APIView):
    """
    特定のuser_idのユーザープロフィールを取得するビュー
    """

    # todo: IsAuthenticatedに変更する
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        operation_id="get_users_retrieve",
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="A user profile",
                response=serializers.UsersSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                constants.UserFields.ID: 2,
                                constants.UserFields.USERNAME: "username1",
                                constants.PlayerFields.DISPLAY_NAME: "display_name1",
                            },
                        },
                    ),
                ],
            ),
            404: utils.OpenApiResponse(
                description="The user does not exist.",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.ERRORS: {"type": "dict"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 404 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.ERRORS: {
                                "user_id": "The user does not exist."
                            },
                        },
                    ),
                ],
            ),
        },
    )
    def get(self, request: request.Request, user_id: int) -> response.Response:
        """
        特定のuser_idのユーザープロフィールを取得するGETメソッド

        Args:
            user_id: URLから取得したユーザーのID
        """
        try:
            # user_idに紐づくPlayerを取得
            player: models.Player = models.Player.objects.get(user_id=user_id)
            users_serializer: serializers.UsersSerializer = (
                serializers.UsersSerializer(
                    player,
                    # emailは含めない
                    fields=(
                        constants.UserFields.ID,
                        constants.UserFields.USERNAME,
                        constants.PlayerFields.DISPLAY_NAME,
                    ),
                )
            )
            return custom_response.CustomResponse(
                data=users_serializer.data,
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist:
            # user_idに紐づくPlayerが存在しない場合
            return custom_response.CustomResponse(
                errors={"user_id": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # MultipleObjectsReturnedなどの場合
            return custom_response.CustomResponse(
                errors={"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
