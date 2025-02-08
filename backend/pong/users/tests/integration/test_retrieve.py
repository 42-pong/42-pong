from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants
from accounts.player import models
from pong.custom_response import custom_response

ID: Final[str] = constants.UserFields.ID
USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = constants.PlayerFields.AVATAR

DATA: Final[str] = custom_response.DATA
ERRORS: Final[str] = custom_response.ERRORS


class UsersRetrieveViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """

        def _create_user_and_related_player(
            user_data: dict, player_data: dict
        ) -> tuple[User, models.Player]:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            player: models.Player = models.Player.objects.create(**player_data)
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

    def tearDown(self) -> None:
        """
        APITestCaseのtearDownメソッドのオーバーライド
        作成したPlayerはplayer.delete()でアバター画像を明示的に削除する必要がある
        """
        for player in (self.player1, self.player2):
            player.delete()

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
            response_data: dict = response.data[DATA]
            self.assertEqual(response_data[ID], user.id)
            self.assertEqual(response_data[USERNAME], user_data[USERNAME])
            self.assertEqual(
                response_data[DISPLAY_NAME], player_data[DISPLAY_NAME]
            )
            self.assertNotIn(EMAIL, response_data)
            self.assertEqual(
                response_data[AVATAR],
                user.player.avatar.url,
            )

    def test_get_404_user_returns_404_with_nonexistent_user_id(self) -> None:
        """
        存在しないuser_idを指定した場合に、エラーが返されることを確認
        """
        not_exist_user_id: int = 1000
        url: str = self._create_url(not_exist_user_id)
        response: drf_response.Response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("user_id", response.data[ERRORS])
