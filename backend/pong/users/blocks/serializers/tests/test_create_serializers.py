from typing import Final

from django.contrib.auth.models import User
from django.test import TestCase

from accounts import constants as accounts_constants
from accounts.player import models as players_models
from users import constants as users_constants

from ... import constants, models
from .. import create_serializers

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
BLOCKED_USER_ID: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER_ID
BLOCKED_USER: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER

CODE_INVALID: Final[str] = users_constants.Code.INVALID
CODE_NOT_EXISTS: Final[str] = users_constants.Code.NOT_EXISTS
CODE_INTERNAL_ERROR: Final[str] = users_constants.Code.INTERNAL_ERROR


class BlockRelationshipCreateSerializerTests(TestCase):
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

    def test_valid_block_relationship_create(self) -> None:
        """
        正常にブロックできることを確認
        """
        # user1がuser2をブロックする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        create_serializer: create_serializers.BlockRelationshipCreateSerializer = create_serializers.BlockRelationshipCreateSerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        # validate()確認
        self.assertTrue(create_serializer.is_valid())
        self.assertEqual(
            create_serializer.validated_data,
            {BLOCKED_USER: {ID: self.user2.id}},
        )
        # create()確認
        create_serializer.save()
        self.assertEqual(
            create_serializer.data,
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
        )

    def test_error_same_user(self) -> None:
        """
        自分自身をブロックしようとした場合にエラーになることを確認
        """
        # user1が自分自身をブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user1.id,
        }
        create_serializer: create_serializers.BlockRelationshipCreateSerializer = create_serializers.BlockRelationshipCreateSerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(create_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, create_serializer.errors)
        self.assertEqual(
            create_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_INTERNAL_ERROR,
        )

    def test_error_already_block(self) -> None:
        """
        既にブロックしているユーザーをブロックしようとした場合にエラーになることを確認
        """
        # user1がuser2をブロックする
        models.BlockRelationship.objects.create(
            user=self.user1, blocked_user=self.user2
        )
        # 再度、user1がuser2をブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        create_serializer: create_serializers.BlockRelationshipCreateSerializer = create_serializers.BlockRelationshipCreateSerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(create_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, create_serializer.errors)
        self.assertEqual(
            create_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_INVALID,
        )

    def test_not_exist_block_user(self) -> None:
        """
        存在しないユーザーをブロックしようとした場合にエラーになることを確認
        """
        # user1が存在しないユーザーをブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: 9999,
        }
        create_serializer: create_serializers.BlockRelationshipCreateSerializer = create_serializers.BlockRelationshipCreateSerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(create_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, create_serializer.errors)
        self.assertEqual(
            create_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_NOT_EXISTS,
        )

    # todo: requestから取得するblocked_user_idがNoneの場合のテストを追加(今は自動でcode="null"が返る)

    def test_error_not_player(self) -> None:
        """
        紐づくPlayerが存在しないユーザー(superuser含む)をブロックしようとした場合にエラーになることを確認
        """
        # user2に紐づくPlayer情報のみ削除
        players_models.Player.objects.get(user=self.user2).delete()
        # user1が、Player情報を持たないuser2をブロックしようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: self.user2.id,
        }
        create_serializer: create_serializers.BlockRelationshipCreateSerializer = create_serializers.BlockRelationshipCreateSerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(create_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, create_serializer.errors)
        self.assertEqual(
            create_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_NOT_EXISTS,
        )
