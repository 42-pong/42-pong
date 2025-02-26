from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from pong.custom_pagination import custom_pagination
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

COUNT: Final[str] = custom_pagination.PaginationFields.COUNT
NEXT: Final[str] = custom_pagination.PaginationFields.NEXT
PREVIOUS: Final[str] = custom_pagination.PaginationFields.PREVIOUS
RESULTS: Final[str] = custom_pagination.PaginationFields.RESULTS


class UsersListViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """

        def _create_user_and_related_player(
            user_data: dict, player_data: dict
        ) -> tuple[User, player_models.Player]:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            player: player_models.Player = player_models.Player.objects.create(
                **player_data
            )
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
        setUp()の情報で2人のユーザーを作成できることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

    def test_200_get_users_list(self) -> None:
        """
        存在するユーザーのプロフィール一覧を取得できることを確認
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
                        ID: self.user1.id,
                        USERNAME: self.user_data1[USERNAME],
                        DISPLAY_NAME: self.player_data1[DISPLAY_NAME],
                        AVATAR: self.player1.avatar.url,
                        IS_FRIEND: False,
                        IS_BLOCKED: False,
                        MATCH_WINS: 0,
                        MATCH_LOSSES: 0,
                    },
                    {
                        ID: self.user2.id,
                        USERNAME: self.user_data2[USERNAME],
                        DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                        AVATAR: self.player2.avatar.url,
                        IS_FRIEND: False,
                        IS_BLOCKED: False,
                        MATCH_WINS: 0,
                        MATCH_LOSSES: 0,
                    },
                ],
            },
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

    def test_get_401_no_users_exist(self) -> None:
        """
        ユーザーが存在しない場合はログインユーザーもいないので、401になりauthentication_failedが返ることを確認
        """
        User.objects.all().delete()
        response: drf_response.Response = self.client.get(
            self.url, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "authentication_failed")
