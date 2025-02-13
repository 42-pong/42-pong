from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models
from pong.custom_response import custom_response

ID: Final[str] = accounts_constants.UserFields.ID
USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = accounts_constants.PlayerFields.AVATAR

DATA: Final[str] = custom_response.DATA


class UsersListViewTests(test.APITestCase):
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

        self.url: str = reverse("users:list")

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

    def test_create_user(self) -> None:
        """
        setUp()の情報で2人のユーザーを作成できることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

    def test_200_no_users_exist(self) -> None:
        """
        ユーザーが存在しない場合、エラーにならず空のプロフィール一覧を取得できることを確認
        """
        User.objects.all().delete()
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[DATA], {})

    def test_200_get_users_list(self) -> None:
        """
        存在するユーザーのプロフィール一覧を取得できることを確認
        """
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            [
                {
                    ID: self.user1.id,
                    USERNAME: self.user_data1[USERNAME],
                    DISPLAY_NAME: self.player_data1[DISPLAY_NAME],
                    AVATAR: self.player1.avatar.url,
                },
                {
                    ID: self.user2.id,
                    USERNAME: self.user_data2[USERNAME],
                    DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                    AVATAR: self.player2.avatar.url,
                },
            ],
        )

    # todo: IsAuthenticatedにしたら、test_401_unauthenticated_user()を追加
