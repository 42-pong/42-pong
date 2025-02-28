from typing import Final
from unittest import mock

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

USER_ID: Final[str] = constants.BlockRelationshipFields.USER_ID
BLOCKED_USER_ID: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER_ID
BLOCKED_USER: Final[str] = constants.BlockRelationshipFields.BLOCKED_USER

CODE_INVALID: Final[str] = users_constants.Code.INVALID
CODE_NOT_EXISTS: Final[str] = users_constants.Code.NOT_EXISTS
CODE_INTERNAL_ERROR: Final[str] = users_constants.Code.INTERNAL_ERROR

MOCK_AVATAR_NAME: Final[str] = "avatars/sample.png"


class BlockRelationshipDestroySerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        """

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value=MOCK_AVATAR_NAME,
        )
        def _create_user(
            user_data: dict, player_data: dict, mock_identicon: mock.MagicMock
        ) -> User:
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

        # user1がuser2をブロック
        self.block_relationship: models.BlockRelationship = (
            models.BlockRelationship.objects.create(
                user=self.user1, blocked_user=self.user2
            )
        )

    def test_valid_block_relationship_destroy(self) -> None:
        """
        正常にブロック解除ができることを確認
        """
        block_relationship_data: dict = {BLOCKED_USER_ID: self.user2.id}
        destroy_serializer: destroy_serializers.BlockRelationshipDestroySerializer = destroy_serializers.BlockRelationshipDestroySerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        # validate()確認
        self.assertTrue(destroy_serializer.is_valid())
        self.assertEqual(
            destroy_serializer.validated_data,
            {BLOCKED_USER: {ID: self.user2.id}},
        )
        # destroy()確認
        block_relationship: models.BlockRelationship = (
            models.BlockRelationship.objects.get(
                user=self.user1, blocked_user=self.user2
            )
        )
        block_relationship.delete()
        self.assertFalse(
            models.BlockRelationship.objects.filter(
                user=self.user1, blocked_user=self.user2
            ).exists()
        )

    def test_error_same_user(self) -> None:
        """
        自分自身をブロック解除しようとした場合にエラーが発生することを確認
        """
        # user1が自分自身をブロック解除しようとする
        block_relationship_data: dict = {BLOCKED_USER_ID: self.user1.id}
        destroy_serializer: destroy_serializers.BlockRelationshipDestroySerializer = destroy_serializers.BlockRelationshipDestroySerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_INTERNAL_ERROR,
        )

    def test_error_already_not_block(self) -> None:
        """
        ブロックしていないユーザーをブロック解除しようとした場合にエラーが発生することを確認
        """
        # user1がuser2をブロック解除する
        self.block_relationship.delete()
        # user1が再度user2をブロック解除しようとする
        block_relationship_data: dict = {BLOCKED_USER_ID: self.user2.id}
        destroy_serializer: destroy_serializers.BlockRelationshipDestroySerializer = destroy_serializers.BlockRelationshipDestroySerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_INVALID,
        )

    def test_error_not_exist_block_user(self) -> None:
        """
        存在しないユーザーをブロック解除しようとした場合にエラーが発生することを確認
        """
        # user1が、存在しないユーザーをブロック解除しようとする
        block_relationship_data: dict = {
            BLOCKED_USER_ID: 9999
        }  # 存在しないユーザー
        destroy_serializer: destroy_serializers.BlockRelationshipDestroySerializer = destroy_serializers.BlockRelationshipDestroySerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_NOT_EXISTS,
        )

    def test_error_not_player(self) -> None:
        """
        紐づくPlayerが存在しないユーザー(superuser含む)をブロック解除しようとした場合にエラーになることを確認
        """
        # user2に紐づくPlayer情報のみ削除
        players_models.Player.objects.get(user=self.user2).delete()
        # user1が、Player情報を持たないuser2をブロック解除しようとする
        block_relationship_data: dict = {BLOCKED_USER_ID: self.user2.id}
        destroy_serializer: destroy_serializers.BlockRelationshipDestroySerializer = destroy_serializers.BlockRelationshipDestroySerializer(
            data=block_relationship_data, context={USER_ID: self.user1.id}
        )

        self.assertFalse(destroy_serializer.is_valid())
        self.assertIn(BLOCKED_USER_ID, destroy_serializer.errors)
        self.assertEqual(
            destroy_serializer.errors[BLOCKED_USER_ID][0].code,
            CODE_NOT_EXISTS,
        )
