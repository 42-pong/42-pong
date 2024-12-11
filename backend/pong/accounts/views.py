from rest_framework import status

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountCreateView(APIView):
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return Response(
            {"message": "Hello, World!"}, status=status.HTTP_200_OK
        )
