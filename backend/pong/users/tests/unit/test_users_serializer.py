import io
from typing import Final
from unittest import mock

import parameterized  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.test import TestCase
from PIL import Image

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from users.blocks import models as blocks_models
from users.friends import constants as friends_constants
from users.friends import models as friends_models

from ... import constants, serializers

ID: Final[str] = accounts_constants.UserFields.ID
USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = accounts_constants.PlayerFields.AVATAR
IS_FRIEND: Final[str] = constants.UsersFields.IS_FRIEND
IS_BLOCKED: Final[str] = constants.UsersFields.IS_BLOCKED
MATCH_WINS: Final[str] = constants.UsersFields.MATCH_WINS
MATCH_LOSSES: Final[str] = constants.UsersFields.MATCH_LOSSES

USER_ID: Final[str] = friends_constants.FriendshipFields.USER_ID

MOCK_AVATAR_NAME: Final[str] = "avatars/sample.png"


class UsersSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        2つのUserと、そのUserに紐づく2つのPlayerをDBに保存
        """

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value=MOCK_AVATAR_NAME,
        )
        def _create_user_and_related_player(
            user_data: dict, player_data: dict, mock_identicon: mock.MagicMock
        ) -> tuple[User, player_models.Player]:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            player: player_models.Player = player_models.Player.objects.create(
                **player_data
            )
            return user, player

        self.user_data_1: dict = {
            USERNAME: "testuser_1",
            EMAIL: "testuser_1@example.com",
            PASSWORD: "testpassword",
        }
        self.user_data_2: dict = {
            USERNAME: "testuser_2",
            EMAIL: "testuser_2@example.com",
            PASSWORD: "testpassword",
        }
        self.player_data_1: dict = {DISPLAY_NAME: "display_name1"}
        self.player_data_2: dict = {DISPLAY_NAME: "display_name2"}
        self.user_1, self.player_1 = _create_user_and_related_player(
            self.user_data_1, self.player_data_1
        )
        self.user_2, self.player_2 = _create_user_and_related_player(
            self.user_data_2, self.player_data_2
        )

    def test_valid_multiple_instance(self) -> None:
        """
        正常なインスタンスが複数渡された場合に、dataにインスタンス分の値が入っていることを確認
        """
        # Userに紐づくPlayer全てのQuerySetを取得
        all_players_with_users: QuerySet[player_models.Player] = (
            player_models.Player.objects.select_related(USER).all()
        )
        # serializer作成
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            all_players_with_users,
            many=True,
            context={USER_ID: self.user_1.id},
        )

        self.assertEqual(
            serializer.data,
            [
                {
                    ID: self.user_1.id,
                    USERNAME: self.user_data_1[USERNAME],
                    EMAIL: self.user_data_1[EMAIL],
                    DISPLAY_NAME: self.player_data_1[DISPLAY_NAME],
                    AVATAR: self.player_1.avatar.url,
                    IS_FRIEND: False,
                    IS_BLOCKED: False,
                    MATCH_WINS: 0,
                    MATCH_LOSSES: 0,
                },
                {
                    ID: self.user_2.id,
                    USERNAME: self.user_data_2[USERNAME],
                    EMAIL: self.user_data_2[EMAIL],
                    DISPLAY_NAME: self.player_data_2[DISPLAY_NAME],
                    AVATAR: self.player_2.avatar.url,
                    IS_FRIEND: False,
                    IS_BLOCKED: False,
                    MATCH_WINS: 0,
                    MATCH_LOSSES: 0,
                },
            ],
        )

    def test_non_users(self) -> None:
        """
        ユーザーが存在しない場合に、エラーにならずdataが空であることを確認
        """
        # User,紐づくPlayerを全て削除
        User.objects.all().delete()

        all_players_with_users: QuerySet[player_models.Player] = (
            player_models.Player.objects.select_related(USER).all()
        )
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            all_players_with_users,
            many=True,
            context={USER_ID: self.user_1.id},
        )

        self.assertEqual(serializer.data, [])

    def test_update_with_valid_display_name(self) -> None:
        """
        正しいdisplay_nameでupdate()が呼ばれた際に、正常にDBのdisplay_nameを更新できることを確認
        """
        # 新しいdisplay_name
        new_valid_display_name: str = "new_name"
        request_data: dict = {
            DISPLAY_NAME: new_valid_display_name,
        }
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player_1,
            data=request_data,
            partial=True,
            context={USER_ID: self.user_1.id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()  # update()が呼ばれる

        self.player_1.refresh_from_db()  # 最新のDBの情報に更新
        self.assertEqual(self.player_1.display_name, new_valid_display_name)

    @parameterized.parameterized.expand(
        [
            ("空文字列のdisplay_name", ""),
            ("max_lengthを超えるdisplay_name", "a" * 16),
            ("不正な文字が含まれるdisplay_name", "あ"),
            ("不正な記号が含まれるdisplay_name", "/"),
        ]
    )
    def test_update_with_invalid_display_name(
        self, testcase_name: str, new_invalid_display_name: str
    ) -> None:
        """
        不正な形式のdisplay_nameでupdate()しようとした際に、エラーが発生して更新されないことを確認
        正しいdisplay_name:
            - 1文字以上、15文字以下
            - 使用可能な文字である英文字・数字・記号(-_.~)で構成される

        Args:
            testcase_name: テストケースの説明
            new_invalid_display_name: 新しく更新したいdisplay_nameの値
        """
        request_data: dict = {
            DISPLAY_NAME: new_invalid_display_name,
        }
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player_1,
            data=request_data,
            partial=True,
            context={USER_ID: self.user_1.id},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(DISPLAY_NAME, serializer.errors)
        # 更新されずに元のdisplay_nameが保持されていることを確認
        self.player_1.refresh_from_db()  # 最新のDBの情報に更新
        self.assertEqual(
            self.player_1.display_name, self.player_data_1[DISPLAY_NAME]
        )

    def test_set_valid_default_avatar(self) -> None:
        """
        serializerのフィールドにデフォルトのavatarパスが設定されていることを確認
        """
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player_1,
            partial=True,
            context={USER_ID: self.user_1.id},
        )

        self.assertEqual(serializer.data[AVATAR], self.player_1.avatar.url)

    def _create_image(self, file_name: str, size: int) -> SimpleUploadedFile:
        image: Image.Image = Image.new("RGB", (30, 30))
        image_io: io.BytesIO = io.BytesIO()
        image.save(image_io, format="PNG")
        # サイズ調整のため、sizeになるまでデータを追加
        image_io.write(b"0" * (size - image_io.tell()))
        image_io.seek(0)
        return SimpleUploadedFile(
            file_name, image_io.read(), content_type="image/png"
        )

    def test_update_with_valid_avatar(self) -> None:
        """
        正常なavatarの場合にエラーにならないことを確認
        (実際の更新はファイルをアップロードしてしまうので今はしない)
        """
        # 最大ファイルサイズ200KBの画像
        valid_image_size: int = 200 * 1024
        new_avatar: SimpleUploadedFile = self._create_image(
            "valid_filename.png", valid_image_size
        )
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player_1,
            data={AVATAR: new_avatar},
            partial=True,
            context={USER_ID: self.user_1.id},
        )

        self.assertTrue(serializer.is_valid())

    def test_update_with_invalid_avatar(self) -> None:
        """
        不正なavatarファイルサイズの場合にエラーになることを確認
        """
        # 最大ファイルサイズ200KBを超える画像
        invalid_image_size: int = 200 * 1024 + 1
        new_avatar: SimpleUploadedFile = self._create_image(
            "valid_filename.png", invalid_image_size
        )
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player_1,
            data={AVATAR: new_avatar},
            partial=True,
            context={USER_ID: self.user_1.id},
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(AVATAR, serializer.errors)

    def test_is_friend(self) -> None:
        """
        フレンドに追加するとis_friendがTrue、フレンド関係を削除するとFalseになることを確認
        """
        # user1がuser2をフレンドに追加
        friendship: friends_models.Friendship = (
            friends_models.Friendship.objects.create(
                user=self.user_1, friend=self.user_2
            )
        )
        # user2のPlayerを取得
        friend_player: player_models.Player = player_models.Player.objects.get(
            user=self.user_2
        )
        # user1をログインユーザーとしてserializer作成
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            friend_player,
            context={USER_ID: self.user_1.id},
        )
        # is_friendがTrueになっていることを確認
        self.assertTrue(serializer.data[IS_FRIEND])

        # フレンド関係を削除
        friendship.delete()
        serializer = serializers.UsersSerializer(
            friend_player,
            context={USER_ID: self.user_1.id},
        )
        # is_friendがFalseになっていることを確認
        self.assertFalse(serializer.data[IS_FRIEND])

    def test_is_blocked(self) -> None:
        """
        ブロックするとis_blockedがTrue、ブロック解除をするとFalseになることを確認
        """
        # user1がuser2をブロック
        block_relationship: blocks_models.BlockRelationship = (
            blocks_models.BlockRelationship.objects.create(
                user=self.user_1, blocked_user=self.user_2
            )
        )
        # user2のPlayerを取得
        blocked_player: player_models.Player = (
            player_models.Player.objects.get(user=self.user_2)
        )
        # user1をログインユーザーとしてserializer作成
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            blocked_player,
            context={USER_ID: self.user_1.id},
        )
        # is_blockedがTrueになっていることを確認
        self.assertTrue(serializer.data[IS_BLOCKED])

        # ブロック解除
        block_relationship.delete()
        serializer = serializers.UsersSerializer(
            blocked_player,
            context={USER_ID: self.user_1.id},
        )
        # is_blockedがFalseになっていることを確認
        self.assertFalse(serializer.data[IS_BLOCKED])
