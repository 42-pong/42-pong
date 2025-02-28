from typing import Final

from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.test import TestCase

from accounts import constants as accounts_constants
from accounts.player import models as players_models
from users import constants as users_constants

from ... import constants, models
from .. import list_serializers

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

USER_ID: Final[str] = constants.FriendshipFields.USER_ID
FRIEND: Final[str] = constants.FriendshipFields.FRIEND


class FriendshipListSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        """

        def _create_user(user_data: dict, player_data: dict) -> User:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            players_models.Player.objects.create(**player_data)
            return user

        # 3人のuserを作成
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
        self.user_data_3: dict = {
            USERNAME: "testuser3",
            EMAIL: "testuser3@example.com",
            PASSWORD: "testpassword",
        }
        self.player_data_1: dict = {
            DISPLAY_NAME: "display_name1",
        }
        self.player_data_2: dict = {
            DISPLAY_NAME: "display_name2",
        }
        self.player_data_3: dict = {
            DISPLAY_NAME: "display_name3",
        }
        self.user1: User = _create_user(self.user_data_1, self.player_data_1)
        self.user2: User = _create_user(self.user_data_2, self.player_data_2)
        self.user3: User = _create_user(self.user_data_3, self.player_data_3)

        # user1が、user2とuser3をフレンドに追加する
        models.Friendship.objects.create(user=self.user1, friend=self.user2)
        models.Friendship.objects.create(user=self.user1, friend=self.user3)

    def test_valid_friendship_list_serializer(self) -> None:
        """
        フレンドが複数存在する場合に、フレンド一覧が取得できることを確認
        """
        # user1のフレンド一覧を取得
        friends: QuerySet[models.Friendship] = (
            models.Friendship.objects.filter(user=self.user1)
        )
        list_serializer: list_serializers.FriendshipListSerializer = (
            list_serializers.FriendshipListSerializer(
                friends, many=True, context={USER_ID: self.user1.id}
            )
        )

        self.assertEqual(
            list_serializer.data,
            [
                {
                    FRIEND: {
                        ID: self.user2.id,
                        USERNAME: self.user_data_2[USERNAME],
                        DISPLAY_NAME: self.player_data_2[DISPLAY_NAME],
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
                        USERNAME: self.user_data_3[USERNAME],
                        DISPLAY_NAME: self.player_data_3[DISPLAY_NAME],
                        AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                        IS_FRIEND: True,
                        IS_BLOCKED: False,
                        MATCH_WINS: 0,
                        MATCH_LOSSES: 0,
                    },
                },
            ],
        )

    def test_empty_friendship_list_serializer(self) -> None:
        """
        フレンドが存在しない場合に、エラーにならず空のフレンド一覧が返されることを確認
        """
        # フレンドがいないuser2のフレンド一覧を取得
        user_id: int = self.user2.id
        friends: QuerySet[models.Friendship] = (
            models.Friendship.objects.filter(user_id=user_id)
        )
        list_serializer: list_serializers.FriendshipListSerializer = (
            list_serializers.FriendshipListSerializer(
                friends, many=True, context={USER_ID: user_id}
            )
        )

        self.assertEqual(list_serializer.data, [])
