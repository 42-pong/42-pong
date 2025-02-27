from typing import Final
from unittest import mock

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from pong.custom_response import custom_response

from ... import constants

ID: Final[str] = accounts_constants.UserFields.ID
USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = accounts_constants.PlayerFields.AVATAR
IS_FRIEND: Final[str] = constants.UsersFields.IS_FRIEND
IS_BLOCKED: Final[str] = constants.UsersFields.IS_BLOCKED
MATCH_WINS: Final[str] = constants.UsersFields.MATCH_WINS
MATCH_LOSSES: Final[str] = constants.UsersFields.MATCH_LOSSES

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE
ERRORS: Final[str] = custom_response.ERRORS

MOCK_AVATAR_NAME: Final[str] = "avatars/sample.png"


class UsersRetrieveViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value=MOCK_AVATAR_NAME,
        )
        def _create_user_and_related_player(
            user_data: dict, player_data: dict, mock_identicon: mock.MagicMock
        ) -> tuple[User, player_models.Player]:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            player: player_models.Player = player_models.Player.objects.create(
                **player_data
            )
            return user, player

        # 1人目のユーザーデータ
        self.user_data1: dict = {
            USERNAME: "testuser1",
            EMAIL: "testuser1@example.com",
            PASSWORD: "password",
        }
        self.player_data1: dict = {
            DISPLAY_NAME: "display_name1",
        }
        # 2人目のユーザーデータ
        self.user_data2: dict = {
            USERNAME: "testuser2",
            EMAIL: "testuser2@example.com",
            PASSWORD: "password",
        }
        self.player_data2: dict = {
            DISPLAY_NAME: "display_name2",
        }

        # 2人のユーザーを作成
        self.user1, self.player1 = _create_user_and_related_player(
            self.user_data1, self.player_data1
        )
        self.user2, self.player2 = _create_user_and_related_player(
            self.user_data2, self.player_data2
        )

        # user1がtokenを取得してログイン
        token_url: str = reverse("jwt:token_obtain_pair")
        token_response: drf_response.Response = self.client.post(
            token_url,
            {
                EMAIL: self.user_data1[EMAIL],
                PASSWORD: self.user_data1[PASSWORD],
            },
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer "
            + token_response.data["data"]["access"]
        )

    def _create_url(self, user_id: int) -> str:
        return reverse("users:retrieve", kwargs={"user_id": user_id})

    def test_create_user(self) -> None:
        """
        setUp()の情報で2人のユーザーを作成できることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

    def test_get_200_user_with_valid_user_id(self) -> None:
        """
        存在するuser_idをurlに指定して特定のユーザープロフィールを取得できることを確認
        """
        for user_data, player_data, user in (
            (self.user_data1, self.player_data1, self.user1),
            (self.user_data2, self.player_data2, self.user2),
        ):
            url: str = self._create_url(user.id)
            response: drf_response.Response = self.client.get(
                url, format="json"
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response.data[DATA],
                {
                    ID: user.id,
                    USERNAME: user_data[USERNAME],
                    DISPLAY_NAME: player_data[DISPLAY_NAME],
                    AVATAR: user.player.avatar.url,
                    IS_FRIEND: False,
                    IS_BLOCKED: False,
                    MATCH_WINS: 0,
                    MATCH_LOSSES: 0,
                },
            )

    def test_get_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーが自分のプロフィールを取得しようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()
        url: str = self._create_url(self.user1.id)
        response: drf_response.Response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_get_404_nonexistent_user_id(self) -> None:
        """
        存在しないuser_idを指定した場合に、エラーが返されることを確認
        """
        not_exist_user_id: int = 1000
        url: str = self._create_url(not_exist_user_id)
        response: drf_response.Response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[CODE], [constants.Code.INTERNAL_ERROR])
        self.assertIn("user_id", response.data[ERRORS])
