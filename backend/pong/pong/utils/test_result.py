from typing import TypeVar

from django.test import TestCase

from .result import Result

T = TypeVar("T")  # 成功結果の型
E = TypeVar("E")  # エラー結果の型


class ResultTests(TestCase):
    """
    Result classのunit test
    """

    def _assert_result_ok(self, value: T) -> None:
        """
        Result.ok()が成功状態で返す値を確認
        """
        result: Result[T, None] = Result.ok(value)

        self.assertTrue(result.is_ok)
        self.assertEqual(result.unwrap(), value)

    def test_result_ok_int(self) -> None:
        """
        Result.ok()でint型の値を正常にラップできることを確認
        """
        self._assert_result_ok(42)

    def test_result_ok_str(self) -> None:
        """
        Result.ok()でstr型の値を正常にラップできることを確認
        """
        self._assert_result_ok("abcde")

    def test_result_ok_list(self) -> None:
        """
        Result.ok()でlist型の値を正常にラップできることを確認
        """
        self._assert_result_ok([1, 2, 3])
