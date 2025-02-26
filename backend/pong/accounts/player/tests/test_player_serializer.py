import io
from typing import Final

import parameterized  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from ... import constants
from .. import models, serializers

USERNAME: Final[str] = constants.UserFields.USERNAME
EMAIL: Final[str] = constants.UserFields.EMAIL
PASSWORD: Final[str] = constants.UserFields.PASSWORD
USER: Final[str] = constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = constants.PlayerFields.DISPLAY_NAME
AVATAR: Final[str] = constants.PlayerFields.AVATAR


class PlayerSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        各テストメソッドの実行前に毎回自動実行される
        """
        self.user_data = {
            USERNAME: "testuser_1",
            EMAIL: "testuser_1@example.com",
            PASSWORD: "testpassword",
        }

    def _create_user(self, user_data: dict) -> User:
        """
        Userを作成するヘルパーメソッド
        """
        user: User = User.objects.create_user(**user_data)
        return user

    def _create_player(
        self, player_data: dict
    ) -> tuple[models.Player, serializers.PlayerSerializer]:
        """
        Playerを作成するヘルパーメソッド
        """
        player_serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=player_data)
        )
        if not player_serializer.is_valid():
            # この関数ではerrorにならない想定
            raise AssertionError(player_serializer.errors)
        player: models.Player = player_serializer.save()
        return player, player_serializer

    def _create_account(
        self, user_data: dict
    ) -> tuple[models.Player, serializers.PlayerSerializer]:
        """
        Userと紐づくPlayerを作成するヘルパーメソッド
        """
        user: User = self._create_user(user_data)
        player_data: dict = {
            USER: user.id,
        }
        player, player_serializer = self._create_player(player_data)
        return player, player_serializer

    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_valid_data(self) -> None:
        """
        正常なデータが渡された場合にエラーにならないことを確認する
        """
        user: User = self._create_user(self.user_data)
        player_data: dict = {
            USER: user.id,
        }
        serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=player_data)
        )

        self.assertTrue(serializer.is_valid())

    def test_create(self) -> None:
        """
        PlayerSerializerのcreate()が、正常にPlayerを作成できることを確認する
        """
        player, player_serializer = self._create_account(self.user_data)
        data: dict = player_serializer.data

        self.assertEqual(data[USER], player.user.id)
        self.assertEqual(data[DISPLAY_NAME], "default")
        self.assertEqual(data[AVATAR], player.avatar.url)

    def test_multi_create(self) -> None:
        """
        PlayerSerializerのcreate()メソッドが複数回呼ばれた場合に、
        正常に全てのPlayerが作成されることを確認する
        """
        # 2人目のアカウント情報
        user_data_2: dict = {
            USERNAME: "testuser_2",
            EMAIL: "testuser_2@example.com",
            PASSWORD: "testpassword",
        }

        # 2人共アカウントを作成し,UserとPlayerが正常に1対1で紐づいているか確認
        for user_data in (self.user_data, user_data_2):
            player, player_serializer = self._create_account(user_data)
            data: dict = player_serializer.data

            self.assertEqual(data[USER], player.user.id)
            self.assertEqual(data[DISPLAY_NAME], "default")
            self.assertEqual(data[AVATAR], player.avatar.url)

    def test_default_display_name(self) -> None:
        """
        display_nameが指定されていない場合、初期値の"default"が自動で設定されることを確認
        """
        _, player_serializer = self._create_account(self.user_data)

        self.assertEqual(
            player_serializer.validated_data[DISPLAY_NAME], "default"
        )

    def test_valid_display_name(self) -> None:
        """
        使用可能な文字列から構成される正常なdisplay_nameが渡された場合に、その値でPlayerが作成されることを確認
        """
        player_data: dict = {
            USER: self._create_user(self.user_data).id,
            DISPLAY_NAME: "abcDEF12345-_.~",  # 正常な15文字のdisplay_name
        }
        _, player_serializer = self._create_player(player_data)

        self.assertEqual(
            player_serializer.validated_data[DISPLAY_NAME],
            player_data[DISPLAY_NAME],
        )

    def _create_image(self, file_name: str) -> SimpleUploadedFile:
        image: Image.Image = Image.new("RGB", (30, 30))
        image_io: io.BytesIO = io.BytesIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)
        return SimpleUploadedFile(
            file_name, image_io.read(), content_type="image/png"
        )

    @parameterized.parameterized.expand(
        [
            ("拡張子が.pngの場合", "test1.png"),
            ("拡張子が.jpgの場合", "test2.jpg"),
            ("拡張子が.jpegの場合", "test3.jpeg"),
            ("拡張子が.gifの場合", "test4.gif"),
            ("ファイル名が最大長の場合", "a" * (50 - len(".png")) + ".png"),
        ]
    )
    def test_valid_avatar_filename(
        self, testcase_name: str, valid_file_name: str
    ) -> None:
        """
        正常なファイル名のavatarが渡された場合にエラーにならないことを確認
        """
        file: SimpleUploadedFile = self._create_image(valid_file_name)
        player_data: dict = {
            USER: self._create_user(self.user_data).id,
            AVATAR: file,
        }
        player_serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=player_data)
        )

        self.assertTrue(player_serializer.is_valid())

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    @parameterized.parameterized.expand(
        [
            ("空文字列のdisplay_name", ""),
            ("max_lengthを超えるdisplay_name", "a" * 16),
            ("不正な文字が含まれるdisplay_name", "あ"),
            ("不正な記号が含まれるdisplay_name", "/"),
        ]
    )
    def test_invalid_display_name(
        self, testcase_name: str, display_name: str
    ) -> None:
        """
        不正なdisplay_nameが渡された場合に、エラーになることを確認
        正しいdisplay_name:
            - 1文字以上、15文字以下
            - 使用可能な文字である英文字・数字・記号(-_.~)で構成される

        Args:
            testcase_name: テストケースの説明
            display_name: display_nameにセットする値
        """
        player_data: dict = {
            USER: self._create_user(self.user_data).id,
            DISPLAY_NAME: display_name,  # 不正なdisplay_name
        }
        player_serializer: serializers.PlayerSerializer = (
            serializers.PlayerSerializer(data=player_data)
        )

        self.assertFalse(player_serializer.is_valid())
        self.assertIn(DISPLAY_NAME, player_serializer.errors)
