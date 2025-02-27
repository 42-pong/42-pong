from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as players_models
from pong.custom_pagination import custom_pagination
from pong.custom_response import custom_response
from users import constants as users_constants

from ... import constants, models

ID: Final[str] = accounts_constants.UserFields.ID
USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = accounts_constants.PlayerFields.AVATAR
IS_FRIEND: Final[str] = users_constants.UsersFields.IS_FRIEND
IS_BLOCKED: Final[str] = users_constants.UsersFields.IS_BLOCKED
MATCH_WINS: Final[str] = users_constants.UsersFields.MATCH_WINS
MATCH_LOSSES: Final[str] = users_constants.UsersFields.MATCH_LOSSES

FRIEND: Final[str] = constants.FriendshipFields.FRIEND

DATA: Final[str] = custom_response.DATA

COUNT: Final[str] = custom_pagination.PaginationFields.COUNT
NEXT: Final[str] = custom_pagination.PaginationFields.NEXT
PREVIOUS: Final[str] = custom_pagination.PaginationFields.PREVIOUS
RESULTS: Final[str] = custom_pagination.PaginationFields.RESULTS


class FriendsListViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """
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

        # 3人のuserを作成
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
        self.user_data3: dict = {
            USERNAME: "testuser3",
            EMAIL: "testuser3@example.com",
            PASSWORD: "password",
        }
        self.player_data1: dict = {
            DISPLAY_NAME: "display_name1",
        }
        self.player_data2: dict = {
            DISPLAY_NAME: "display_name2",
        }
        self.player_data3: dict = {
            DISPLAY_NAME: "display_name3",
        }
        self.user1, self.player1 = _create_user_and_related_player(
            self.user_data1, self.player_data1
        )
        self.user2, self.player2 = _create_user_and_related_player(
            self.user_data2, self.player_data2
        )
        self.user3, self.player3 = _create_user_and_related_player(
            self.user_data3, self.player_data3
        )

        # user1が、user2とuser3をフレンドに追加する
        self.friendship1: models.Friendship = models.Friendship.objects.create(
            user=self.user1, friend=self.user2
        )
        self.friendship2: models.Friendship = models.Friendship.objects.create(
            user=self.user1, friend=self.user3
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

    def test_create_user(self) -> None:
        """
        setUp()の情報で3人のユーザーを作成できることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())
        self.assertTrue(User.objects.filter(id=self.user3.id).exists())

    def test_200_no_friends_exist(self) -> None:
        """
        自分のフレンドが存在しない場合、エラーにならず空のフレンド一覧を取得できることを確認
        """
        # フレンドを全員削除
        self.user2.delete()
        self.user3.delete()
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {COUNT: 0, NEXT: None, PREVIOUS: None, RESULTS: []},
        )

    def test_200_get_friends_list(self) -> None:
        """
        自分のフレンドのユーザープロフィール一覧を取得できることを確認
        """
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 2,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: [
                    {
                        FRIEND: {
                            ID: self.user2.id,
                            USERNAME: self.user_data2[USERNAME],
                            DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                            AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                            IS_FRIEND: True,
                            IS_BLOCKED: False,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                    {
                        FRIEND: {
                            ID: self.user3.id,
                            USERNAME: self.user_data3[USERNAME],
                            DISPLAY_NAME: self.player_data3[DISPLAY_NAME],
                            AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                            IS_FRIEND: True,
                            IS_BLOCKED: False,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                ],
            },
        )

    def test_200_delete_friend(self) -> None:
        """
        フレンドから削除した場合にフレンド一覧からも削除されることを確認
        """
        # user1がuser2をフレンドから削除
        self.friendship1.delete()
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user3のみフレンド一覧に残る
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 1,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: [
                    {
                        FRIEND: {
                            ID: self.user3.id,
                            USERNAME: self.user_data3[USERNAME],
                            DISPLAY_NAME: self.player_data3[DISPLAY_NAME],
                            AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                            IS_FRIEND: True,
                            IS_BLOCKED: False,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                ],
            },
        )

    def test_200_exists_non_player(self) -> None:
        """
        紐づくPlayerが存在しないユーザー(superuser含む)はフレンド一覧に含まれないことを確認
        """
        # user3をフレンドから削除はせず、紐づくPlayer情報のみ削除
        players_models.Player.objects.get(user=self.user3).delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user2のみフレンド一覧に表示される
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 1,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: [
                    {
                        FRIEND: {
                            ID: self.user2.id,
                            USERNAME: self.user_data2[USERNAME],
                            DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                            AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                            IS_FRIEND: True,
                            IS_BLOCKED: False,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                ],
            },
        )

    def test_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーがフレンド一覧を取得しようとするとエラーになることを確認
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
