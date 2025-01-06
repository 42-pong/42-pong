from django.test import TestCase

from oauth2 import serializers


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        """
        unittest.TestCaseのsetUpメソッドをオーバーライドして、テスト実行前に必要な初期設定を行う関数

        初期設定
        - self.SerializerにUserSerializerのインスタンスを代入
        """
        self.Serializer: serializers.UserSerializer = (
            serializers.UserSerializer
        )

    # todo: パスワードに文字列を入力した場合のテストを書く?（現状だとパスワードの値は入る）
    #       その場合は関数名を変更する。
    def test_valid_serializer(self) -> None:
        """
        正しいデータが与えられた場合、UserSerializerが正しく機能するかを確認するテスト

        テスト項目
        - シリアライザが有効であること
        - 検証されたデータが期待通りであること
        - シリアライズされたデータが期待通りであること
        - シリアライザにエラーがないこと
        """

        # passwordが空文字を想定
        user_data: dict = {
            "id": 1,
            "username": "pong",
            "email": "pong@gmail.com",
            "password": "",
        }
        serializer: serializers.UserSerializer = self.Serializer(
            data=user_data
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data,
            {"username": "pong", "email": "pong@gmail.com", "password": ""},
        )
        self.assertEqual(
            serializer.data, {"username": "pong", "email": "pong@gmail.com"}
        )
        self.assertTrue(serializer.errors == {})



class OAuth2SerializerTestCase(TestCase):
    def setUp(self) -> None:
        # self.user = User.objects.create_user()
        self.Serializer = serializers.OAuth2Serializer

    def test_true(self) -> None:
        self.assertTrue(True)


class FortyTwoTokenSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # self.oauth2 = OAuth2.objects.create()
        self.Serializer = serializers.FortyTwoTokenSerializer

    def test_true(self) -> None:
        self.assertTrue(True)
