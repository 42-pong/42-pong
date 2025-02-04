from typing import Final

from django.contrib.auth.models import User
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
