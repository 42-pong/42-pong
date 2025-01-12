import unittest

from parameterized import parameterized  # type: ignore
from rest_framework import serializers

from match.serializers.ws_serializer import WebsocketInputSerializer


class TestWebsocketSerializer(unittest.TestCase):
    """
    websocket 全イベント共通のmessageスキーマ用のシリアライザ―のバリデーションのテスト
    """

    @parameterized.expand(
        [
            (
                "MATCHカテゴリーがvalidか",
                {"category": "MATCH", "payload": {}},
            ),
            # TODO: イベントを追加したらテストケースを追加する
        ]
    )
    def test_valid_message(self, name: str, message: dict) -> None:
        """
        メッセージ形式が正しい時に、エラーが例外が発生しないか確認
        """
        try:
            serializer = WebsocketInputSerializer(data=message)
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # 例外が発生した場合、エラーメッセージを出力してアサート
            self.fail(f"Validation failed: {str(e)}")
        else:
            # 例外が発生しなかった場合、成功とみなす
            self.assertTrue(True)

    @parameterized.expand(
        [
            (
                "存在しないカテゴリー",
                {
                    "category": "INVALID_CATEGORY",
                    "payload": {},
                },
                "invalid_choice",
            ),
            (
                "スキーマの必須keyがない",
                {
                    "category": "MATCH",
                    "invalid_key": {},
                },
                "required",
            ),
            (
                "スキーマに加えて余計なdataが入っている",
                {
                    "category": "MATCH",
                    "payload": {},
                    "waste": {"waste_key": "waste_data"},
                },
                "invalid",
            ),
        ]
    )
    def test_invalid_message(
        self, name: str, message: dict, error_code: str
    ) -> None:
        """
        メッセージ形式が不正な時に、エラーが例外が発生しないか確認

        Args:
            name (str): テストケースの説明
            message (dict): テストデータ
            error_code (str): ValidationErrorが返すエラーコード

        error_code:
            required = 必要なフィールドがない
            invalid = 必要なキーがない
            invalid_choice = キーのChoiceフィールドが不正
        """
        serializer = WebsocketInputSerializer(data=message)

        # 例外が発生することを確認
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        # ValidationErrorが発生した場合、そのエラーコードを確認
        self.assertTrue(error_code, context.exception.get_codes())
