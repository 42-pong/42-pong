from django.contrib.auth.models import AnonymousUser, User
from django.db.models.query import QuerySet
from rest_framework import permissions, request, response, status, viewsets

from pong.custom_response import custom_response

from . import models
from .serializers import list_serializers


# todo: 各メソッドにtry-exceptを書いて予期せぬエラー(実装上のミスを含む)の場合に500を返す
class FriendsViewSet(viewsets.ModelViewSet):
    queryset = models.Friendship.objects.all().select_related("user", "friend")
    permission_classes = (permissions.IsAuthenticated,)

    http_method_names = ["get"]

    def list(self, request: request.Request) -> response.Response:
        """
        自分のフレンドのユーザープロフィール一覧を取得するGETメソッド
        """
        user: User | AnonymousUser = request.user
        if isinstance(user, AnonymousUser):
            return custom_response.CustomResponse(
                errors={"user": "The user does not exist."},
                status=status.HTTP_404_NOT_FOUND,  # todo: 404ではないかも
            )

        # 自分のフレンド一覧を取得
        friends: QuerySet[models.Friendship] = self.queryset.filter(user=user)
        list_serializer: list_serializers.FriendshipListSerializer = (
            list_serializers.FriendshipListSerializer(friends, many=True)
        )
        return custom_response.CustomResponse(
            data=list_serializer.data, status=status.HTTP_200_OK
        )
