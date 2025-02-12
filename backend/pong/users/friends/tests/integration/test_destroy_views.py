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
CODE_INTERNAL_ERROR: Final[str] = users_constants.Code.INTERNAL_ERROR


class FriendsListViewTests(test.APITestCase):
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

        # user1が、user2をフレンドに追加する
        self.friendship: models.Friendship = models.Friendship.objects.create(
            user=self.user1, friend=self.user2
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

    def _create_url(self, friend_id: int) -> str:
        # /api/*/{id}/ の形の場合はdetail
        return reverse(
            "users:friends:friends-detail", kwargs={"friend_id": friend_id}
        )

    def test_204_delete_friend(self) -> None:
        """
        フレンドを正常にフレンドから削除できることを確認
        """
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data[DATA], {})
        self.assertFalse(
            models.Friendship.objects.filter(
                user=self.user1, friend=self.user2
            ).exists()
        )

    def test_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーがフレンド一覧を取得しようとするとエラーになることを確認
        """
        # user1の認証情報をクリア
        self.client.credentials()
        # ログインしていないuser1がuser2をフレンドから削除しようとする
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_404_delete_non_friend(self) -> None:
        """
        フレンドでないユーザーをフレンドから削除しようとするとエラーになることを確認
        """
        # user1がuser2をフレンドから削除
        self.friendship.delete()
        # 再度user1がuser2をフレンドから削除しようとする
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user2.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[CODE][0], CODE_INVALID)
        self.assertFalse(
            models.Friendship.objects.filter(
                user=self.user1, friend=self.user2
            ).exists()
        )

    def test_404_delete_same_user(self) -> None:
        """
        自分自身をフレンドから削除しようとするとエラーになることを確認
        """
        # user1が自分自身をフレンドから削除
        response: drf_response.Response = self.client.delete(
            self._create_url(self.user1.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data[CODE][0], CODE_INTERNAL_ERROR)
