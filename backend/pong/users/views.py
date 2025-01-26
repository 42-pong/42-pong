from drf_spectacular import utils
from rest_framework import (
    permissions,
    request,
    response,
    status,
    views,
)

from pong.custom_response import custom_response


class UsersListView(views.APIView):
    """
    ユーザープロフィールの一覧を取得するビュー
    """

    # todo: IsAuthenticatedに変更する
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=None,
        responses={
            200: utils.OpenApiResponse(
                description="A list of user profiles",
                response={"type": "object"},  # todo: serializerに変える
                examples=[
                    utils.OpenApiExample(
                        "Example 200 response",
                        value={
                            "status": "ok",
                            "data": [
                                {
                                    "id": 2,
                                    "username": "username1",
                                    # todo: display_name,avatar追加
                                },
                                {
                                    "id": 3,
                                    "username": "username2",
                                    # todo: display_name,avatar追加
                                },
                                {"...", "..."},
                            ],
                        },
                    ),
                ],
            ),
        },
    )
    def get(self, request: request.Request) -> response.Response:
        """
        ユーザープロフィール一覧を取得するGETメソッド
        """
        return custom_response.CustomResponse(status=status.HTTP_200_OK)
