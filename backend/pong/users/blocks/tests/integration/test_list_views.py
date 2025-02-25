from typing import Final
from unittest import mock

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

BLOCKED_USER: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER

DATA: Final[str] = custom_response.DATA

COUNT: Final[str] = custom_pagination.PaginationFields.COUNT
NEXT: Final[str] = custom_pagination.PaginationFields.NEXT
PREVIOUS: Final[str] = custom_pagination.PaginationFields.PREVIOUS
RESULTS: Final[str] = custom_pagination.PaginationFields.RESULTS

MOCK_AVATAR_NAME: Final[str] = "avatars/sample.png"


class BlocksListViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """
        self.url: str = reverse("users:blocks:blocks-list")

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value=MOCK_AVATAR_NAME,
        )
        def _create_user_and_related_player(
            user_data: dict, player_data: dict, mock_identicon: mock.MagicMock
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

        # user1が、user2とuser3をブロックする
        self.block_relationship1: models.BlockRelationship = (
            models.BlockRelationship.objects.create(
                user=self.user1, blocked_user=self.user2
            )
        )
        self.block_relationship2: models.BlockRelationship = (
            models.BlockRelationship.objects.create(
                user=self.user1, blocked_user=self.user3
            )
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

    def test_create_user(self) -> None:
        """
        setUp()の情報で3人のユーザーを作成できることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())
        self.assertTrue(User.objects.filter(id=self.user3.id).exists())

    def test_200_no_block_user(self) -> None:
        """
        誰もブロックしていない場合、エラーにならず空のブロック一覧を取得できることを確認
        """
        # ブロックしているユーザーを全員ブロック解除
        self.block_relationship1.delete()
        self.block_relationship2.delete()
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {COUNT: 0, NEXT: None, PREVIOUS: None, RESULTS: []},
        )

    def test_200_get_block_list(self) -> None:
        """
        自分がブロックしているユーザープロフィール一覧を取得できることを確認
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
                        BLOCKED_USER: {
                            ID: self.user2.id,
                            USERNAME: self.user_data2[USERNAME],
                            DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                            AVATAR: self.player2.avatar.url,
                            IS_FRIEND: False,
                            IS_BLOCKED: True,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                    {
                        BLOCKED_USER: {
                            ID: self.user3.id,
                            USERNAME: self.user_data3[USERNAME],
                            DISPLAY_NAME: self.player_data3[DISPLAY_NAME],
                            AVATAR: self.player3.avatar.url,
                            IS_FRIEND: False,
                            IS_BLOCKED: True,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                ],
            },
        )

    def test_200_delete_block_user(self) -> None:
        """
        ブロック解除をした場合にブロック一覧からも削除されることを確認
        """
        # user1がuser2のブロックを解除
        self.block_relationship1.delete()
        response: drf_response.Response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user3のみブロック一覧に残る
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 1,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: [
                    {
                        BLOCKED_USER: {
                            ID: self.user3.id,
                            USERNAME: self.user_data3[USERNAME],
                            DISPLAY_NAME: self.player_data3[DISPLAY_NAME],
                            AVATAR: self.player3.avatar.url,
                            IS_FRIEND: False,
                            IS_BLOCKED: True,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                ],
            },
        )

    def test_200_exists_non_player(self) -> None:
        """
        紐づくPlayerが存在しないユーザー(superuser含む)はブロック一覧に含まれないことを確認
        """
        # user3をブロック解除はせず、紐づくPlayer情報のみ削除
        players_models.Player.objects.get(user=self.user3).delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # user2のみブロック一覧に表示される
        self.assertEqual(
            response.data[DATA],
            {
                COUNT: 1,
                NEXT: None,
                PREVIOUS: None,
                RESULTS: [
                    {
                        BLOCKED_USER: {
                            ID: self.user2.id,
                            USERNAME: self.user_data2[USERNAME],
                            DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                            AVATAR: self.player2.avatar.url,
                            IS_FRIEND: False,
                            IS_BLOCKED: True,
                            MATCH_WINS: 0,
                            MATCH_LOSSES: 0,
                        },
                    },
                ],
            },
        )

    def test_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーがブロック一覧を取得しようとするとエラーになることを確認
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
