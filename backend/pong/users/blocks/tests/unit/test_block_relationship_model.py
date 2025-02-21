from typing import Final

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts import constants

from ... import models

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD


class BlockRelationshipModelTestCase(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        """

        def _create_user(user_data: dict) -> User:
            return User.objects.create_user(**user_data)

        #  user1: user
        self.user_data1: dict = {
            USERNAME: "testuser1",
            EMAIL: "testuser1@example.com",
            PASSWORD: "testpassword",
        }
        # user2: blocked_user
        self.user_data2: dict = {
            USERNAME: "testuser2",
            EMAIL: "testuser2@example.com",
            PASSWORD: "testpassword",
        }
        # 2人のUserを作成
        self.user1: User = _create_user(self.user_data1)
        self.user2: User = _create_user(self.user_data2)

        # user1がuser2をブロックした、というBlockRelationshipを作成
        self.block_relationship: models.BlockRelationship = (
            models.BlockRelationship.objects.create(
                user=self.user1,
                blocked_user=self.user2,
            )
        )

    def test_setup_create_success(self) -> None:
        """
        念のためuserが2人、BlockRelationshipが1つ作成されたことを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())
        self.assertTrue(
            models.BlockRelationship.objects.filter(
                id=self.block_relationship.id
            ).exists()
        )

    def test_valid_related_user(self) -> None:
        """
        作成したBlockRelationshipが正しく2人のuserに紐づいていることを確認
        """
        user_id: int = self.block_relationship.user.id
        user: User = User.objects.get(id=user_id)
        # BlockRelationshipから取得したuserがuser1と一致することを確認
        self.assertEqual(user.username, self.user_data1[USERNAME])

        blocked_user_id: int = self.block_relationship.blocked_user.id
        blocked_user: User = User.objects.get(id=blocked_user_id)
        # BlockRelationshipから取得したblocked_userがuser2と一致することを確認
        self.assertEqual(blocked_user.username, self.user_data2[USERNAME])

    def test_delete_block_relationship(self) -> None:
        """
        BlockRelationshipを削除しても、userは削除されないことを確認
        """
        block_relationship_id: int = self.block_relationship.id
        # BlockRelationship削除
        self.block_relationship.delete()

        # BlockRelationshipが削除されていることを確認
        self.assertFalse(
            models.BlockRelationship.objects.filter(
                id=block_relationship_id
            ).exists()
        )
        # userが2人とも削除されていないことを確認
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

    def test_delete_related_user(self) -> None:
        """
        userを削除すると、BlockRelationshipも削除されることを確認
        """
        user_id: int = self.user1.id
        blocked_user_id: int = self.user2.id
        block_relationship_id: int = self.block_relationship.id
        # user1を削除
        self.user1.delete()

        # BlockRelationshipが削除されていることを確認
        self.assertFalse(
            models.BlockRelationship.objects.filter(
                id=block_relationship_id
            ).exists()
        )
        # user1は削除され、user2は削除されていないことを確認
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertTrue(User.objects.filter(id=blocked_user_id).exists())

    def test_delete_related_blocked_user(self) -> None:
        """
        blocked_userを削除すると、BlockRelationshipも削除されることを確認
        """
        user_id: int = self.user1.id
        blocked_user_id: int = self.user2.id
        block_relationship_id: int = self.block_relationship.id
        # user2を削除
        self.user2.delete()

        # BlockRelationshipが削除されていることを確認
        self.assertFalse(
            models.BlockRelationship.objects.filter(
                id=block_relationship_id
            ).exists()
        )
        # user1は削除されておらず、user2は削除されていることを確認
        self.assertTrue(User.objects.filter(id=user_id).exists())
        self.assertFalse(User.objects.filter(id=blocked_user_id).exists())

    def test_reverse_block_relationship(self) -> None:
        """
        user2が自分をブロックする、という逆のBlockRelationshipであれば作成できることを確認
        """
        block_relationship: models.BlockRelationship = (
            models.BlockRelationship.objects.create(
                user=self.user2,
                blocked_user=self.user1,
            )
        )

        self.assertTrue(
            models.BlockRelationship.objects.filter(
                id=block_relationship.id
            ).exists()
        )
        self.assertEqual(models.BlockRelationship.objects.count(), 2)

    def test_error_duplicate_block_relationship(self) -> None:
        """
        同じBlockRelationshipは作成できないことを確認
        """
        with self.assertRaises(ValidationError):
            models.BlockRelationship.objects.create(
                user=self.user1,
                blocked_user=self.user2,
            )
        self.assertEqual(models.BlockRelationship.objects.count(), 1)

    def test_error_self_block_relationship(self) -> None:
        """
        自分自身をブロックするBlockRelationshipは作成できないことを確認
        """
        with self.assertRaises(ValidationError):
            models.BlockRelationship.objects.create(
                user=self.user1,
                blocked_user=self.user1,
            )
        self.assertEqual(models.BlockRelationship.objects.count(), 1)
