import unittest
from typing import Final

from parameterized import parameterized  # type: ignore
from rest_framework import serializers

from match.serializers.match_serializer import MatchInputSerializer

REQUIRED: Final[str] = "required"
INVALID: Final[str] = "invalid"
INVALID_CHOICE: Final[str] = "invalid_choice"


class TestMatchSerializer(unittest.TestCase):
    """
    matchイベントのメッセージスキーマのバリデーションテスト
    MatchInputSerializer.is_valid(raise_exception=True)
    実際にraise_exception=Trueで使用しているので、テストでもそれで実行する
    """

    @parameterized.expand(
        [
            # ============================
            # 正しいスキーマのテストケース
            # ============================
            (
                "正しいINITステージのメッセージ",
                {
                    "stage": "INIT",
                    "data": {"mode": "REMOTE"},
                },
            ),
            (
                "正しいREADYステージのメッセージ",
                {
                    "stage": "READY",
                    "data": {},
                },
            ),
            (
                "正しいPLAYステージのメッセージ",
                {
                    "stage": "PLAY",
                    "data": {"move": "UP", "team": "1"},
                },
            ),
            (
                "正しいENDステージのメッセージ",
                {"stage": "END", "data": {}},
            ),
        ]
    )
    def test_valid_message(self, name: str, payload: dict) -> None:
        """
        正しいスキーマが通るか確かめるテスト

        Args:
            name (str): テストケースの説明
            payload (dict): テストデータ
        """
        try:
            serializer = MatchInputSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # 例外が発生した場合、エラーメッセージを出力してアサート
            self.fail(f"Validation failed: {str(e)}")
        else:
            # 例外が発生せずにvalidation後のデータが入っていれば成功とみなす
            self.assertTrue(serializer.validated_data)

    @parameterized.expand(
        [
            # ============================
            # 不正なスキーマのテストケース
            # ============================
            (
                "正しいmatchスキーマに加えて余計なデータが入っている",
                {
                    "stage": "READY",
                    "data": {},
                    "waste": {"waste_key": "waste_data"},
                },
                INVALID,
            ),
            # INITステージ
            (
                "INITステージの中身が空",
                {"stage": "INIT", "data": {}},
                REQUIRED,
            ),
            (
                "INITステージの中身に余計なものが入っている",
                {
                    "stage": "INIT",
                    "data": {"mode": "LOCAL", "waste_key": "waste_data"},
                },
                INVALID,
            ),
            (
                "INITステージのmode keyが不正",
                {"stage": "INIT", "data": {"MoDe": "REMOTE"}},
                REQUIRED,
            ),
            (
                "INITステージのmode keyの値が空",
                {"stage": "INIT", "data": {"mode": ""}},
                INVALID_CHOICE,
            ),
            # READYステージ
            (
                "READYステージの中身に余計なものが入っている",
                {
                    "stage": "READY",
                    "data": {"waste_key": "waste_data"},
                },
                INVALID,
            ),
            # PLAYステージ
            (
                "PLAYステージのkeyが不正",
                {"stage": "PLAY", "data": {"move": "UP", "TeAm": "1"}},
                REQUIRED,
            ),
            (
                "PLAYステージにの値に不要なものが入っている",
                {
                    "stage": "PLAY",
                    "data": {
                        "move": "UP",
                        "team": "1",
                        "waste_key": "waste_data",
                    },
                },
                INVALID,
            ),
            (
                "PLAYステージのteam keyの値が不正",
                {
                    "stage": "PLAY",
                    "data": {"move": "DOWN", "team": "-1"},
                },
                INVALID_CHOICE,
            ),
            # ENDステージ
            (
                "ENDステージのteam keyの値が不正",
                {
                    "stage": "END",
                    "data": {"waste_key": "waste_data"},
                },
                INVALID,
            ),
        ]
    )
    def test_invalid_message(
        self, name: str, payload: dict, error_code: str
    ) -> None:
        """
        不正なスキーマが通るか確かめるテスト

        Args:
            name (str): テストケースの説明
            payload (dict): テストデータ
            error_code (str): ValidationErrorが返すエラーコード

        error_code:
            required = 必要なフィールドがない
            invalid = 必要なキーがない
            invalid_choice = キーのChoiceフィールドが不正
        """
        serializer = MatchInputSerializer(data=payload)
        # 例外が発生することを確認
        with self.assertRaises(serializers.ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        # ValidationErrorが発生した場合、そのエラーコードを確認
        # error_dictの型が複雑（dictの中にlistや文字列がある）ので、strに変換して確認
        error_dict = context.exception.get_codes()
        self.assertTrue(
            error_code in str(error_dict),
            f"'{error_code}' not found in {error_dict}",
        )
