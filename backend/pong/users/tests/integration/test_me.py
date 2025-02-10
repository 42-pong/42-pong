from typing import Final

import parameterized  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from pong.custom_response import custom_response

from ... import constants

USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE
ERRORS: Final[str] = custom_response.ERRORS


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
        self.user: User = User.objects.create_user(**self.user_data)
        self.player_data[USER] = self.user
        self.player: player_models.Player = (
            player_models.Player.objects.create(**self.player_data)
        )

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

    def test_setup_create_user(self) -> None:
        """
        念のため、setUp()でUser,Playerが作成できていることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user.id).exists())
        self.assertTrue(
            player_models.Player.objects.filter(id=self.player.id).exists()
        )

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
        self.assertEqual(response_data[EMAIL], self.user_data[EMAIL])
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
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_patch_200_update_valid_display_name(self) -> None:
        """
        正しいdisplay_nameを送り、自分のdisplay_nameを更新できることを確認
        """
        new_valid_display_name: str = "new_name"
        response: drf_response.Response = self.client.patch(
            self.url,
            {DISPLAY_NAME: new_valid_display_name},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: dict = response.data[DATA]
        self.assertEqual(response_data[DISPLAY_NAME], new_valid_display_name)
        # 最新のDBの情報に更新し、DBの値も変更されていることを確認
        self.player.refresh_from_db()
        self.assertEqual(self.player.display_name, new_valid_display_name)

    @parameterized.parameterized.expand(
        [
            ("空文字列のdisplay_name", ""),
            ("max_lengthを超えるdisplay_name", "a" * 16),
            ("不正な文字が含まれるdisplay_name", "あ"),
            ("不正な記号が含まれるdisplay_name", "/"),
        ]
    )
    def test_patch_400_update_invalid_display_name(
        self, testcase_name: str, new_invalid_display_name: str
    ) -> None:
        """
        不正なdisplay_nameを送ると、自分のdisplay_nameを更新せずエラーになることを確認
        """
        response: drf_response.Response = self.client.patch(
            self.url,
            {DISPLAY_NAME: new_invalid_display_name},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[CODE], [constants.Code.INVALID])
        self.assertIn(DISPLAY_NAME, response.data[ERRORS])
        # 最新のDBの情報に更新し、DBの値が変更されていないことを確認
        self.player.refresh_from_db()
        self.assertEqual(
            self.player.display_name, self.player_data[DISPLAY_NAME]
        )

    def test_patch_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーが自分のプロフィールを更新しようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()
        new_valid_display_name: str = "new_name"
        response: drf_response.Response = self.client.patch(
            self.url,
            {DISPLAY_NAME: new_valid_display_name},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")
