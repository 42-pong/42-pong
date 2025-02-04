from typing import Final

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts import constants

from .. import models

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD


class FriendshipModelTestCase(TestCase):
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
        # user2: friend
        self.user_data2: dict = {
            USERNAME: "testuser2",
            EMAIL: "testuser2@example.com",
            PASSWORD: "testpassword",
        }
        # 2人のUserを作成
        self.user1: User = _create_user(self.user_data1)
        self.user2: User = _create_user(self.user_data2)

        # user1が自分のフレンドにuser2を追加した、というFriendship作成
        self.friendship: models.Friendship = models.Friendship.objects.create(
            user=self.user1,
            friend=self.user2,
        )

    def test_setup_create_success(self) -> None:
        """
        念のためuserが2人、Friendshipが1つ作成されたことを確認
        """
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())
        self.assertTrue(
            models.Friendship.objects.filter(id=self.friendship.id).exists()
        )

    def test_valid_related_user(self) -> None:
        """
        作成したFriendshipが正しく2人のuserに紐づいていることを確認
        """
        user_id: int = self.friendship.user.id
        user: User = User.objects.get(id=user_id)
        # Friendshipから取得したuserがuser1と一致することを確認
        self.assertEqual(user.username, self.user_data1[USERNAME])

        friend_id: int = self.friendship.friend.id
        friend: User = User.objects.get(id=friend_id)
        # Friendshipから取得したfriendがuser2と一致することを確認
        self.assertEqual(friend.username, self.user_data2[USERNAME])

    def test_delete_friendship(self) -> None:
        """
        Friendshipを削除しても、userは削除されないことを確認
        """
        friendship_id: int = self.friendship.id
        # Friendship削除
        self.friendship.delete()

        # Friendshipが削除されていることを確認
        self.assertFalse(
            models.Friendship.objects.filter(id=friendship_id).exists()
        )
        # userが2人とも削除されていないことを確認
        self.assertTrue(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())

    def test_delete_related_user(self) -> None:
        """
        userを削除すると、Friendshipも削除されることを確認
        """
        user_id: int = self.user1.id
        friend_id: int = self.user2.id
        friendship_id: int = self.friendship.id
        # user1を削除
        self.user1.delete()

        # Friendshipが削除されていることを確認
        self.assertFalse(
            models.Friendship.objects.filter(id=friendship_id).exists()
        )
        # user1は削除され、user2は削除されていないことを確認
        self.assertFalse(User.objects.filter(id=user_id).exists())
        self.assertTrue(User.objects.filter(id=friend_id).exists())

    def test_delete_related_friend(self) -> None:
        """
        friendを削除すると、Friendshipも削除されることを確認
        """
        user_id: int = self.user1.id
        friend_id: int = self.user2.id
        friendship_id: int = self.friendship.id
        # user2を削除
        self.user2.delete()

        # Friendshipが削除されていることを確認
        self.assertFalse(
            models.Friendship.objects.filter(id=friendship_id).exists()
        )
        # user1は削除されておらず、user2は削除されていることを確認
        self.assertTrue(User.objects.filter(id=user_id).exists())
        self.assertFalse(User.objects.filter(id=friend_id).exists())

    def test_reverse_friendship(self) -> None:
        """
        user2が自分のフレンドにuser1を追加する、という逆のFriendshipであれば作成できることを確認
        """
        friendship: models.Friendship = models.Friendship.objects.create(
            user=self.user2,
            friend=self.user1,
        )
        self.assertTrue(
            models.Friendship.objects.filter(id=friendship.id).exists()
        )
        self.assertEqual(models.Friendship.objects.count(), 2)

    def test_error_duplicate_friendship(self) -> None:
        """
        同じFriendshipは作成できないことを確認
        """
        with self.assertRaises(ValidationError):
            models.Friendship.objects.create(
                user=self.user1,
                friend=self.user2,
            )
        self.assertEqual(models.Friendship.objects.count(), 1)
