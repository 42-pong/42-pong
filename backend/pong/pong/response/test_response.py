from typing import Final

from django import test
from rest_framework import status

from . import response as custom_response

STATUS: Final[str] = custom_response.STATUS
DATA: Final[str] = custom_response.DATA
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
        response: custom_response.Response = custom_response.Response()

        self.assertEqual(response.status, status.HTTP_200_OK)
        self.assertEqual(response.data, {STATUS: STATUS_OK, DATA: {}})

    def test_201_with_data(self) -> None:
        """
        201で呼ばれた際に、成功レスポンスが形式に沿って返されることを確認
        """
        response: custom_response.Response = custom_response.Response(
            data={"key": "value"}, status=status.HTTP_201_CREATED
        )

        self.assertEqual(response.status, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data, {STATUS: STATUS_OK, DATA: {"key": "value"}}
        )

    def test_400_with_errors(self) -> None:
        """
        400で呼ばれた際に、エラーレスポンスが形式に沿って返されることを確認
        """
        response: custom_response.Response = custom_response.Response(
            errors={"key": "value"},
            status=status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {STATUS: STATUS_ERROR, ERRORS: {"key": "value"}},
        )

    # -------------------------------------------------------------------------
    # エラーケース
    # -------------------------------------------------------------------------
    def test_invalid_status(self) -> None:
        """
        100-599以外のステータスコードが渡された場合に例外が発生することを確認
        """
        with self.assertRaises(ValueError):
            custom_response.Response(status=99)

        with self.assertRaises(ValueError):
            custom_response.Response(status=600)
