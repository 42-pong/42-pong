from typing import Final

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as players_models
from pong.custom_response import custom_response
from users import constants as users_constants

from ... import models

USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE

CODE_INVALID: Final[str] = users_constants.Code.INVALID
CODE_NOT_EXISTS: Final[str] = users_constants.Code.NOT_EXISTS
CODE_INTERNAL_ERROR: Final[str] = users_constants.Code.INTERNAL_ERROR


class BlocksDestroyViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
        """

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

        # user1が、user2をブロックする
        self.block_relationship: models.BlockRelationship = (
            models.BlockRelationship.objects.create(
                user=self.user1, blocked_user=self.user2
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

    def _create_url(self, blocked_user_id: int) -> str:
        # /api/*/{id}/ の形の場合はdetail
        return reverse(
            "users:blocks:blocks-detail",
            kwargs={"blocked_user_id": blocked_user_id},
        )

    def test_204_delete_block(self) -> None:
        """
        正常にブロック解除をできることを確認
        """
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data[DATA], {})
        self.assertFalse(
            models.BlockRelationship.objects.filter(
                user=self.user1, blocked_user=self.user2
            ).exists()
        )

    def test_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーがブロック解除しようとするとエラーになることを確認
        """
        # user1の認証情報をクリア
        self.client.credentials()
        # ログインしていないuser1がuser2をブロック解除しようとする
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_404_delete_not_block(self) -> None:
        """
        ブロックしていないユーザーをブロック解除しようとするとエラーになることを確認
        """
        # user1がuser2をブロック解除する
        self.block_relationship.delete()
        # 再度user1がuser2をブロック解除しようとする
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[CODE][0], CODE_INVALID)
        self.assertFalse(
            models.BlockRelationship.objects.filter(
                user=self.user1, blocked_user=self.user2
            ).exists()
        )

    def test_404_delete_same_user(self) -> None:
        """
        自分自身をブロック解除しようとするとエラーになることを確認
        """
        # user1が自分自身をブロック解除
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user1.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[CODE][0], CODE_INTERNAL_ERROR)

    def test_404_delete_not_exist_user(self) -> None:
        """
        存在しないユーザーをブロック解除しようとするとエラーになることを確認
        """
        # 存在しないユーザーをブロック解除
        response: drf_response.Response = self.client.delete(
            self._create_url(9999)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[CODE][0], CODE_NOT_EXISTS)

    def test_404_not_player(self) -> None:
        """
        紐づくPlayerが存在しないユーザー(superuser含む)をブロック解除しようとした場合にエラーになることを確認
        """
        # user2に紐づくPlayer情報のみ削除
        players_models.Player.objects.get(user=self.user2).delete()
        # user1が、Player情報を持たないuser2をブロック解除しようとする
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data[CODE][0], users_constants.Code.NOT_EXISTS
        )
