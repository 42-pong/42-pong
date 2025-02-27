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

USER_ID: Final[str] = constants.BlockRelationshipFields.USER_ID
BLOCKED_USER_ID: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER_ID
BLOCKED_USER: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE


class BlocksCreateViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """
        # POSTもlistで取得するらしい
        self.url: str = reverse("users:blocks:blocks-list")

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

    def test_201_valid_block_relationship_create(self) -> None:
        """
        正常にブロックできることを確認
        """
        # user1がuser2をブロックする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, block_relationship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data[DATA],
            {
                BLOCKED_USER: {
                    ID: self.user2.id,
                    USERNAME: self.user_data2[USERNAME],
                    DISPLAY_NAME: self.player_data2[DISPLAY_NAME],
                    AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                    IS_FRIEND: False,
                    IS_BLOCKED: True,
                    MATCH_WINS: 0,
                    MATCH_LOSSES: 0,
                },
            },
        )
        self.assertTrue(
            models.BlockRelationship.objects.filter(
                user=self.user1, blocked_user=self.user2
            ).exists()
        )

    def test_400_invalid_same_user(self) -> None:
        """
        自分自身をブロックしようとした場合にエラーでcode=internal_errorが返ることを確認
        """
        # user1が自分自身をブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user1.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, block_relationship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[CODE][0], users_constants.Code.INTERNAL_ERROR
        )
        self.assertFalse(
            models.BlockRelationship.objects.filter(user=self.user1).exists()
        )

    def test_400_already_block(self) -> None:
        """
        既にブロックしているユーザーをブロックしようとした場合に
        エラーでcode=invalidが返ることを確認
        """
        # user1がuser2をブロックする
        models.BlockRelationship.objects.create(
            user=self.user1, blocked_user=self.user2
        )
        # 再度、user1がuser2をブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, block_relationship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[CODE][0], users_constants.Code.INVALID)
        self.assertTrue(
            models.BlockRelationship.objects.filter(user=self.user1).exists()
        )

    def test_400_not_exist_block_user(self) -> None:
        """
        存在しないユーザーをブロックしようとした場合にエラーcode=not_existsが返ることを確認
        """
        # user1が存在しないユーザーをブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: 9999,
        }
        response: drf_response.Response = self.client.post(
            self.url, block_relationship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[CODE][0], users_constants.Code.NOT_EXISTS
        )
        self.assertFalse(
            models.BlockRelationship.objects.filter(user=self.user1).exists()
        )

    def test_400_not_player(self) -> None:
        """
        紐づくPlayerが存在しないユーザー(superuser含む)をブロックしようとした場合に
        エラーでcode=not_existsが返ることを確認
        """
        # user2に紐づくPlayer情報のみ削除
        players_models.Player.objects.get(user=self.user2).delete()
        # user1が、Player情報を持たないuser2をブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, block_relationship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[CODE][0], users_constants.Code.NOT_EXISTS
        )
        self.assertFalse(
            models.BlockRelationship.objects.filter(user=self.user1).exists()
        )

    def test_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーがブロックしようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()

        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        response: drf_response.Response = self.client.post(
            self.url, block_relationship_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")
