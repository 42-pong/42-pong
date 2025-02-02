from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants
from accounts.player import models as player_models
from pong.custom_response import custom_response

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = constants.PlayerFields.DISPLAY_NAME

DATA: Final[str] = custom_response.DATA


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

    def test_get_200_authenticated_user(self) -> None:
        """
        認証済みユーザーが自分のプロフィールを取得できることを確認
        """
        response: drf_response.Response = self.client.get(
            self.url, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: dict = response.data[DATA]
        self.assertEqual(response_data[USERNAME], self.user_data[USERNAME])
        self.assertEqual(
            response_data[DISPLAY_NAME], self.player_data[DISPLAY_NAME]
        )

    def test_get_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーが自分のプロフィールを取得しようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()
        response: drf_response.Response = self.client.get(
            self.url, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せて変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")
