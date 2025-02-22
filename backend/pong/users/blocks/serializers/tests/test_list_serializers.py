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

USER_ID: Final[str] = constants.BlockRelationshipFields.USER_ID
BLOCKED_USER: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER


class BlockRelationshipListSerializerTests(TestCase):
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

        # user1が、user2とuser3をブロックする
        models.BlockRelationship.objects.create(
            user=self.user1, blocked_user=self.user2
        )
        models.BlockRelationship.objects.create(
            user=self.user1, blocked_user=self.user3
        )

    def test_valid_block_relationship_list_serializer(self) -> None:
        """
        複数人ブロックしている場合に、ブロック一覧が取得できることを確認
        """
        # user1のブロック一覧を取得
        block_users: QuerySet[models.BlockRelationship] = (
            models.BlockRelationship.objects.filter(user=self.user1)
        )
        list_serializer: list_serializers.BlockRelationshipListSerializer = (
            list_serializers.BlockRelationshipListSerializer(
                block_users, many=True, context={USER_ID: self.user1.id}
            )
        )

        self.assertEqual(
            list_serializer.data,
            [
                {
                    BLOCKED_USER: {
                        ID: self.user2.id,
                        USERNAME: self.user_data_2[USERNAME],
                        DISPLAY_NAME: self.player_data_2[DISPLAY_NAME],
                        AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                        IS_FRIEND: False,
                        IS_BLOCKED: True,
                        # todo: is_online,win_match,lose_match追加
                    },
                },
                {
                    BLOCKED_USER: {
                        ID: self.user3.id,
                        USERNAME: self.user_data_3[USERNAME],
                        DISPLAY_NAME: self.player_data_3[DISPLAY_NAME],
                        AVATAR: "/media/avatars/sample.png",  # todo: デフォルト画像が変更になったら修正
                        IS_FRIEND: False,
                        IS_BLOCKED: True,
                        # todo: is_online,win_match,lose_match追加
                    },
                },
            ],
        )

    def test_empty_block_relationship_list_serializer(self) -> None:
        """
        ブロックしているユーザーがいない場合に、エラーにならず空のブロック一覧が返されることを確認
        """
        # 誰もブロックしていないuser2のブロック一覧を取得
        user_id: int = self.user2.id
        block_users: QuerySet[models.BlockRelationship] = (
            models.BlockRelationship.objects.filter(user=user_id)
        )
        list_serializer: list_serializers.BlockRelationshipListSerializer = (
            list_serializers.BlockRelationshipListSerializer(
                block_users, many=True, context={USER_ID: user_id}
            )
        )

        self.assertEqual(list_serializer.data, [])
