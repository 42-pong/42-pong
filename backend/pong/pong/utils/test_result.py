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
        Result.ok()が成功状態で値を返し、unwrap_error()で例外を発生させることを確認
        """
        result: Result[T, None] = Result.ok(value)

        self.assertTrue(result.is_ok)
        self.assertEqual(result.unwrap(), value)
        # Result.ok()の時にunwrap_error()を呼ぶと例外が発生することを確認
        with self.assertRaisesMessage(
            ValueError, f"Called unwrap_error on an ok value: {value}"
        ):
            result.unwrap_error()

    def _assert_result_error(self, value: E) -> None:
        """
        Result.error()がエラー状態で値を返し、unwrap()で例外を発生させることを確認
        """
        result: Result[None, E] = Result.error(value)

        self.assertFalse(result.is_ok)
        self.assertEqual(result.unwrap_error(), value)
        # Result.error()の時にunwrap()を呼ぶと例外が発生することを確認
        with self.assertRaisesMessage(
            ValueError, f"Called unwrap on an error value: {value}"
        ):
            result.unwrap()

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

    def test_result_error_int(self) -> None:
        """
        Result.error()でint型の値を正常にラップできることを確認
        """
        self._assert_result_error(-1)

    def test_result_error_str(self) -> None:
        """
        Result.error()でstr型の値を正常にラップできることを確認
        """
        self._assert_result_error("error message")
