from typing import Final

from django.contrib.auth.models import User
from django.test import TestCase

from accounts import constants as accounts_constants
from accounts.player import models as players_models
from users import constants as users_constants

from ... import constants, models
from .. import destroy_serializers

ID: Final[str] = accounts_constants.UserFields.ID
USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME

USER_ID: Final[str] = constants.FriendshipFields.USER_ID
FRIEND_USER_ID: Final[str] = constants.FriendshipFields.FRIEND_USER_ID
FRIEND: Final[str] = constants.FriendshipFields.FRIEND

CODE_INVALID: Final[str] = users_constants.Code.INVALID
CODE_NOT_EXISTS: Final[str] = users_constants.Code.NOT_EXISTS
CODE_INTERNAL_ERROR: Final[str] = users_constants.Code.INTERNAL_ERROR


class FriendshipCreateSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        """

        def _create_user(user_data: dict, player_data: dict) -> User:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            players_models.Player.objects.create(**player_data)
            return user

        # 2人のuserを作成
        self.user_data_1: dict = {
            USERNAME: "testuser1",
            EMAIL: "testuser1@example.com",
            PASSWORD: "testpassword",
        }
        self.user_data_2: dict = {
            USERNAME: "testuser2",
            EMAIL: "testuser2@example.com",
            PASSWORD: "testpassword",
        }
        self.player_data_1: dict = {
            DISPLAY_NAME: "display_name1",
        }
        self.player_data_2: dict = {
            DISPLAY_NAME: "display_name2",
        }
        self.user1: User = _create_user(self.user_data_1, self.player_data_1)
        self.user2: User = _create_user(self.user_data_2, self.player_data_2)

        # user1がuser2をフレンドに追加
        self.friendship: models.Friendship = models.Friendship.objects.create(
            user=self.user1, friend=self.user2
        )

    def test_valid_friendship_destroy(self) -> None:
        """
        正常にフレンド解除ができることを確認
        """
        friendship_data: dict = {
            USER_ID: self.user1.id,
            FRIEND_USER_ID: self.user2.id,
        }
        destroy_serializer: destroy_serializers.FriendshipDestroySerializer = (
            destroy_serializers.FriendshipDestroySerializer(
                data=friendship_data
            )
        )

        # validate()確認
        self.assertTrue(destroy_serializer.is_valid())
        self.assertEqual(
            destroy_serializer.validated_data,
            {USER: {ID: self.user1.id}, FRIEND: {ID: self.user2.id}},
        )
        # destroy()確認
        friendship: models.Friendship = models.Friendship.objects.get(
            user=self.user1, friend=self.user2
        )
        friendship.delete()
        self.assertFalse(
            models.Friendship.objects.filter(
                user=self.user1, friend=self.user2
            ).exists()
        )

    def test_error_same_user(self) -> None:
        """
        自分自身をフレンド解除しようとした場合にエラーが発生することを確認
        """
        # user1が自分自身をフレンド解除しようとする
        friendship_data: dict = {
            USER_ID: self.user1.id,
            FRIEND_USER_ID: self.user1.id,
        }
        destroy_serializer: destroy_serializers.FriendshipDestroySerializer = (
            destroy_serializers.FriendshipDestroySerializer(
                data=friendship_data
            )
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(FRIEND_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[FRIEND_USER_ID][0].code,
            CODE_INTERNAL_ERROR,
        )

    def test_error_already_not_friend(self) -> None:
        """
        フレンドではないユーザーをフレンド解除しようとした場合にエラーが発生することを確認
        """
        # user1がuser2をフレンド解除する
        self.friendship.delete()
        # user1が再度user2をフレンド解除しようとする
        friendship_data: dict = {
            USER_ID: self.user1.id,
            FRIEND_USER_ID: self.user2.id,
        }
        destroy_serializer: destroy_serializers.FriendshipDestroySerializer = (
            destroy_serializers.FriendshipDestroySerializer(
                data=friendship_data
            )
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(FRIEND_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[FRIEND_USER_ID][0].code,
            CODE_INVALID,
        )

    def test_error_not_exist_friend(self) -> None:
        """
        存在しないユーザーをフレンド解除しようとした場合にエラーが発生することを確認
        """
        # user1が存在しないユーザーをフレンド解除しようとする
        friendship_data: dict = {
            USER_ID: self.user1.id,
            FRIEND_USER_ID: 9999,
        }
        destroy_serializer: destroy_serializers.FriendshipDestroySerializer = (
            destroy_serializers.FriendshipDestroySerializer(
                data=friendship_data
            )
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(FRIEND_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[FRIEND_USER_ID][0].code,
            users_constants.Code.NOT_EXISTS,
        )
