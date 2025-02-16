from typing import Final, Optional

import parameterized  # type: ignore[import-untyped]
from django import test
from rest_framework import status

from . import custom_response

STATUS: Final[str] = custom_response.STATUS
DATA: Final[str] = custom_response.DATA
CODE: Final[str] = custom_response.CODE
ERRORS: Final[str] = custom_response.ERRORS

STATUS_OK: Final[str] = custom_response.Status.OK
STATUS_ERROR: Final[str] = custom_response.Status.ERROR


class ResponseTests(test.TestCase):
    # -------------------------------------------------------------------------
    # 正常ケース
    # -------------------------------------------------------------------------
    def test_200_no_args(self) -> None:
        """
        引数なしで呼ばれた際に、デフォルトのレスポンスが返されることを確認
        """
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse()
        )

        self.assertEqual(response.status, status.HTTP_200_OK)
        self.assertEqual(response.data, {STATUS: STATUS_OK, DATA: {}})

    def test_200_with_empty_data(self) -> None:
        """
        引数にNoneではなく空listが渡された際に、デフォルトの空辞書ではなくそのまま返されることを確認
        """
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse(data=[])
        )

        self.assertEqual(response.status, status.HTTP_200_OK)
        self.assertEqual(response.data, {STATUS: STATUS_OK, DATA: []})

    def test_201_with_data(self) -> None:
        """
        201(デフォルト値の200以外)で呼ばれた際に、成功レスポンスが形式に沿って返されることを確認
        """
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse(
                data={"key": "value"}, status=status.HTTP_201_CREATED
            )
        )

        self.assertEqual(response.status, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {STATUS: STATUS_OK, DATA: {"key": "value"}}
        )

    @parameterized.parameterized.expand(
        [
            ("codeが引数に渡されない場合", None, []),
            ("codeが1つの場合", ["invalid"], ["invalid"]),
            (
                "codeが複数の場合",
                ["invalid1", "invalid2"],
                ["invalid1", "invalid2"],
            ),
        ]
    )
    def test_400_with_code(
        self,
        testcase_name: str,
        code: Optional[list[str]],
        expected_code: Optional[list[str]],
    ) -> None:
        """
        エラー時に400で呼ばれた際に、エラーレスポンスが形式に沿って返されることを確認
        """
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse(
                code=code,
                errors={"key": "value"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        )

        self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                STATUS: STATUS_ERROR,
                CODE: expected_code,
                ERRORS: {"key": "value"},
            },
        )

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_invalid_status(self) -> None:
        """
        100-599以外のステータスコードが渡された場合に例外が発生することを確認
        """
        with self.assertRaises(ValueError):
            custom_response.CustomResponse(status=99)

        with self.assertRaises(ValueError):
            custom_response.CustomResponse(status=600)
