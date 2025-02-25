import io
import os
from typing import Final
from unittest import mock, skip

import parameterized  # type: ignore[import-untyped]
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from rest_framework import response as drf_response
from rest_framework import status, test

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from pong.custom_response import custom_response

from ... import constants

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

DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE
ERRORS: Final[str] = custom_response.ERRORS

AVATAR_DIR: Final[str] = "media/avatars/"
MOCK_AVATAR_NAME: Final[str] = "avatars/sample.png"


class UsersMeViewTests(test.APITestCase):
    def setUp(self) -> None:
        """
        APITestCaseのsetUpメソッドのオーバーライド
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

        # データを用意
        self.user_data: dict = {
            USERNAME: "testuser",
            EMAIL: "testuser@example.com",
            PASSWORD: "password",
        }
        self.player_data: dict = {
            DISPLAY_NAME: "display_name1",
        }
        # User,Playerを作成
        self.user, self.player = _create_user_and_related_player(
            self.user_data, self.player_data
        )

        # tokenを取得
        token_url: str = reverse("simple_jwt:token_obtain_pair")
        token_response: drf_response.Response = self.client.post(
            token_url,
            {
                USERNAME: self.user_data[USERNAME],
                PASSWORD: self.user_data[PASSWORD],
            },
            format="json",
        )
        # access_tokenを使用して認証
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + token_response.data["access"]
        )

        self.url: str = reverse("users:me")

    def test_setup_create_user(self) -> None:
        """
        念のため、setUp()でUser,Playerが作成できていることを確認
        """
        self.assertTrue(User.objects.filter(id=self.user.id).exists())
        self.assertTrue(
            player_models.Player.objects.filter(id=self.player.id).exists()
        )

    def test_get_200_authenticated_user(self) -> None:
        """
        認証済みユーザーが自分のプロフィールを取得できることを確認
        """
        response: drf_response.Response = self.client.get(
            self.url, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[DATA],
            {
                ID: self.user.id,
                USERNAME: self.user_data[USERNAME],
                EMAIL: self.user_data[EMAIL],
                DISPLAY_NAME: self.player_data[DISPLAY_NAME],
                AVATAR: self.player.avatar.url,
                IS_FRIEND: False,
                IS_BLOCKED: False,
                MATCH_WINS: 0,
                MATCH_LOSSES: 0,
            },
        )

    def test_get_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーが自分のプロフィールを取得しようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()
        response: drf_response.Response = self.client.get(
            self.url, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def test_patch_200_update_valid_display_name(self) -> None:
        """
        正しいdisplay_nameを送り、自分のdisplay_nameを更新できることを確認
        """
        new_valid_display_name: str = "new_name"
        response: drf_response.Response = self.client.patch(
            self.url,
            {DISPLAY_NAME: new_valid_display_name},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data: dict = response.data[DATA]
        self.assertEqual(response_data[DISPLAY_NAME], new_valid_display_name)
        # 最新のDBの情報に更新し、DBの値も変更されていることを確認
        self.player.refresh_from_db()
        self.assertEqual(self.player.display_name, new_valid_display_name)

    @parameterized.parameterized.expand(
        [
            ("空文字列のdisplay_name", ""),
            ("max_lengthを超えるdisplay_name", "a" * 16),
            ("不正な文字が含まれるdisplay_name", "あ"),
            ("不正な記号が含まれるdisplay_name", "/"),
        ]
    )
    def test_patch_400_update_invalid_display_name(
        self, testcase_name: str, new_invalid_display_name: str
    ) -> None:
        """
        不正なdisplay_nameを送ると、自分のdisplay_nameを更新せずエラーになることを確認
        """
        response: drf_response.Response = self.client.patch(
            self.url,
            {DISPLAY_NAME: new_invalid_display_name},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[CODE], [constants.Code.INVALID])
        self.assertIn(DISPLAY_NAME, response.data[ERRORS])
        # 最新のDBの情報に更新し、DBの値が変更されていないことを確認
        self.player.refresh_from_db()
        self.assertEqual(
            self.player.display_name, self.player_data[DISPLAY_NAME]
        )

    def test_patch_401_unauthenticated_user(self) -> None:
        """
        認証されていないユーザーが自分のプロフィールを更新しようとするとエラーになることを確認
        """
        # 認証情報をクリア
        self.client.credentials()
        new_valid_display_name: str = "new_name"
        response: drf_response.Response = self.client.patch(
            self.url,
            {DISPLAY_NAME: new_valid_display_name},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # DRFのpermission_classesによりエラーが返るため、自作のResponse formatではない
        # todo: permissions_classesを変更して自作Responseを返せる場合、併せてresponse.data[CODE]を見るように変更する
        self.assertEqual(response.data["detail"].code, "not_authenticated")

    def _create_image(self, file_name: str) -> io.BytesIO:
        image = Image.new("RGB", (30, 30))
        # メモリ上に画像を生成する
        image_io = io.BytesIO()
        image.save(image_io, format="PNG")
        image_io.seek(0)  # ファイルの読み取り位置を先頭に戻す
        image_io.name = file_name
        return image_io

    @skip(
        "デフォルトのアバター画像をmockにしているので新規登録の扱いになりupdate()ではなくcreate()が呼ばれてしまうため、アバター更新のテストは手動で行う"
    )
    # def test_patch_200_update_valid_avatar(self) -> None:
    #     """
    #     正常なファイル名でavatarを更新できることを確認
    #     """
    #     file_name: str = "tmp.png"
    #     image_io: io.BytesIO = self._create_image(file_name)
    #     # multipart/form-dataで送信
    #     response: drf_response.Response = self.client.patch(
    #         self.url,
    #         {AVATAR: image_io},
    #         format="multipart",
    #     )

    #     new_file_name: str = f"{self.user.username}.png"
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(os.path.exists(AVATAR_DIR + new_file_name))
    #     self.player.refresh_from_db()
    #     self.assertEqual(self.player.avatar.name, "avatars/" + new_file_name)
    #     # アバター画像を削除
    #     self.player.avatar.delete()

    @parameterized.parameterized.expand(
        [
            ("空文字列の場合", ""),
            ("拡張子がない場合", "not_exist_extension"),
            ("拡張子が不正な場合", "testuser.invalid_extension"),
        ]
    )
    def test_patch_400_update_invalid_avatar(
        self, testcase_name: str, new_file_name: str
    ) -> None:
        """
        不正なファイル名でavatarを更新しようとするとエラーになることを確認
        """
        image_io: io.BytesIO = self._create_image(new_file_name)
        response: drf_response.Response = self.client.patch(
            self.url,
            {AVATAR: image_io},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[CODE], [constants.Code.INVALID])
        self.assertIn(AVATAR, response.data[ERRORS])
        # 画像がmediaディレクトリに保存されていないことを確認
        if new_file_name:
            self.assertFalse(os.path.exists(AVATAR_DIR + new_file_name))
        # 最新のDBの情報に更新し、DBの値が変更されていないことを確認
        self.player.refresh_from_db()
        self.assertEqual(self.player.avatar.name, MOCK_AVATAR_NAME)
