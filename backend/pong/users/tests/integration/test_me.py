from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import test

from accounts import constants
from accounts.player import models as player_models

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = constants.PlayerFields.DISPLAY_NAME


class UsersMeViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """
        # データを用意
        self.user_data: dict = {
            USERNAME: "testuser",
            EMAIL: "testuser@example.com",
            PASSWORD: "password",
        }
        self.player_data: dict = {
            DISPLAY_NAME: "display_name1",
        }
        # User,Playerを作成
        user = User.objects.create_user(**self.user_data)
        self.player_data[USER] = user
        player_models.Player.objects.create(**self.player_data)

        # tokenを取得
        token_url: str = reverse("tmp_jwt:token_obtain_pair")
        token_response: drf_response.Response = self.client.post(
            token_url,
            {
                USERNAME: self.user_data[USERNAME],
                PASSWORD: self.user_data[PASSWORD],
            },
            format="json",
        )
        # access_tokenを使用して認証
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + token_response.data["access"]
        )

        self.url: str = reverse("users:me")
