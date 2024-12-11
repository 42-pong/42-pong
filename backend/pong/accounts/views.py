from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class AccountCreateView(APIView):
    # todo: try-exceptを書いて予期せぬエラー(実装上のミスを含む)の場合に500を返す
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        # requestをserializerに渡して変換とバリデーションを行う
        serializer: UserSerializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Userを新規作成してDBに追加し、作成された情報を返す
        user = serializer.save()
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )
