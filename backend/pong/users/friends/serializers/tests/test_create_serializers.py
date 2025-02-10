from typing import Final

from django.contrib.auth.models import User
from django.test import TestCase

from accounts import constants as accounts_constants
from accounts.player import models as players_models

from ... import constants
from .. import create_serializers

ID: Final[str] = accounts_constants.UserFields.ID
USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME

USER_ID: Final[str] = constants.FriendshipFields.USER_ID
FRIEND_USER_ID: Final[str] = constants.FriendshipFields.FRIEND_USER_ID
FRIEND: Final[str] = constants.FriendshipFields.FRIEND


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

    def test_valid_friendship_create(self) -> None:
        """
        正常にフレンド追加ができることを確認
        """
        # user1がuser2をフレンドに追加する
        friendship_data: dict = {
            USER_ID: self.user1.id,
            FRIEND_USER_ID: self.user2.id,
        }
        create_serializer: create_serializers.FriendshipCreateSerializer = (
            create_serializers.FriendshipCreateSerializer(data=friendship_data)
        )

        # validate()確認
        self.assertTrue(create_serializer.is_valid())
        self.assertEqual(
            create_serializer.validated_data,
            {USER: {ID: self.user1.id}, FRIEND: {ID: self.user2.id}},
        )
        # create()確認
        create_serializer.save()
        self.assertEqual(
            create_serializer.data,
            {
                USER_ID: self.user1.id,
                FRIEND_USER_ID: self.user2.id,
                FRIEND: {
                    USERNAME: self.user_data_2[USERNAME],
                    DISPLAY_NAME: self.player_data_2[DISPLAY_NAME],
                },
            },
        )

    def test_error_same_user(self) -> None:
        """
        自分自身をフレンドに追加しようとした場合にエラーになることを確認
        """
        # user1が自分自身をフレンドに追加しようとする
        friendship_data: dict = {
            USER_ID: self.user1.id,
            FRIEND_USER_ID: self.user1.id,
        }
        create_serializer: create_serializers.FriendshipCreateSerializer = (
            create_serializers.FriendshipCreateSerializer(data=friendship_data)
        )

        self.assertFalse(create_serializer.is_valid())
        self.assertIn(FRIEND_USER_ID, create_serializer.errors)
        self.assertEqual(
            create_serializer.errors[FRIEND_USER_ID][0].code,
            "internal_error",  # todo: constantsに置き換え
        )
