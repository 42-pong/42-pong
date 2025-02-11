from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as players_models
from pong.custom_response import custom_response
from users import constants as users_constants

from ... import constants, models

USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = accounts_constants.PlayerFields.AVATAR

USER_ID: Final[str] = constants.FriendshipFields.USER_ID
FRIEND_USER_ID: Final[str] = constants.FriendshipFields.FRIEND_USER_ID
FRIEND: Final[str] = constants.FriendshipFields.FRIEND

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE


class FriendsCreateViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """
        # POSTもlistで取得するらしい
        self.url: str = reverse("users:friends:friends-list")

        def _create_user_and_related_player(
            user_data: dict, player_data: dict
        ) -> tuple[User, players_models.Player]:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            player: players_models.Player = (
                players_models.Player.objects.create(**player_data)
            )
            return user, player

        # 2人のuserを作成
        self.user_data1: dict = {
            USERNAME: "testuser1",
            EMAIL: "testuser1@example.com",
            PASSWORD: "password",
        }
        self.user_data2: dict = {
            USERNAME: "testuser2",
            EMAIL: "testuser2@example.com",
            PASSWORD: "password",
        }
        self.player_data1: dict = {
            DISPLAY_NAME: "display_name1",
        }
        self.player_data2: dict = {
            DISPLAY_NAME: "display_name2",
        }
        self.user1, self.player1 = _create_user_and_related_player(
            self.user_data1, self.player_data1
        )
        self.user2, self.player2 = _create_user_and_related_player(
            self.user_data2, self.player_data2
        )

        # user1がtokenを取得してログイン
        # todo: 自作jwtができたらnamespaceを変更
        token_url: str = reverse("simple_jwt:token_obtain_pair")
        token_response: drf_response.Response = self.client.post(
            token_url,
            {
                USERNAME: self.user_data1[USERNAME],
                PASSWORD: self.user_data1[PASSWORD],
            },
            format="json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + token_response.data["access"]
        )

    def test_201_valid_friendship_create(self) -> None:
        """
        正常にフレンド追加ができることを確認
        """
        # user1がuser2をフレンドに追加する
        friendship_data: dict = {
            FRIEND_USER_ID: self.user2.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, friendship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data[DATA],
            {
                USER_ID: self.user1.id,
                FRIEND_USER_ID: self.user2.id,
                FRIEND: {
                    USERNAME: self.user_data2[USERNAME],
                    DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                    AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                },
            },
        )
        self.assertTrue(
            models.Friendship.objects.filter(
                user=self.user1, friend=self.user2
            ).exists()
        )

    def test_400_invalid_same_user(self) -> None:
        """
        自分自身をフレンドに追加しようとした場合にエラーでcode=internal_errorが返ることを確認
        """
        # user1が自分自身をフレンドに追加しようとする
        friendship_data: dict = {
            FRIEND_USER_ID: self.user1.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, friendship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[CODE][0], users_constants.Code.INTERNAL_ERROR
        )
        self.assertFalse(
            models.Friendship.objects.filter(user=self.user1).exists()
        )

    def test_400_already_friend(self) -> None:
        """
        既にフレンドであるユーザーをフレンドに追加しようとした場合に
        エラーでcode=invalidが返ることを確認
        """
        # user1がuser2をフレンドに追加する
        models.Friendship.objects.create(user=self.user1, friend=self.user2)
        # 再度、user1がuser2をフレンドに追加しようとする
        friendship_data: dict = {
            FRIEND_USER_ID: self.user2.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, friendship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[CODE][0], users_constants.Code.INVALID)
        self.assertTrue(
            models.Friendship.objects.filter(user=self.user1).exists()
        )

    def test_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーがフレンド一覧を取得しようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()
        response: drf_response.Response = self.client.post(
            self.url, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")
