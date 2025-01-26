from rest_framework import (
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

    def get(self, request: request.Request) -> response.Response:
        """
        ユーザープロフィール一覧を取得するGETメソッド
        """
        return custom_response.CustomResponse(status=status.HTTP_200_OK)
