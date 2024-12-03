from typing import Generic, TypeVar, Union, cast

T = TypeVar("T")  # 成功時の値の型
E = TypeVar("E")  # エラー時の値の型


class Result(Generic[T, E]):
    """
    成功(ok)または失敗(error)を表現する型
    処理の結果として成功または失敗の状態を保持し、それぞれに関連する値をラップする
    成功時にはT型の値を返し、失敗時にはE型の値を返す

    使用例:
    ```
    def func() -> Result[int, str]:
        if エラーの場合:
            return Result.error("Error: some error occurred")
        # 成功の場合
        success_value: int = 42
        return Result.ok(success_value)


    result: Result[int, str] = func()
    if result.is_ok:
        # 成功時の処理
        print(f"success value: {result.unwrap()}")
    else:
        # エラー時の処理
        print(f"error value: {result.unwrap_error()}")
    ```

    メソッド:
        - `is_ok`       : 成功状態かどうか
        - `is_error`    : エラー状態かどうか
        - `unwrap`      : 成功時の値(T型)を取り出す。エラー時は例外
        - `unwrap_error`: エラー時の値(E型)を取り出す。成功時は例外
        - `ok`          : 成功結果を作成
        - `error`       : エラー結果を作成
    """

    def __init__(self, value: Union[T, E], is_ok: bool):
        self._value = value
        self._is_ok = is_ok

    @property
    def is_ok(self) -> bool:
        return self._is_ok

    @property
    def is_error(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        """
        成功時のみ呼ばれることを前提として、成功時の値(T型)を返す
        もし失敗時(result_error)の状態で呼ばれた場合、例外(ValueError)を発生させる
        """
        if not self._is_ok:
            raise ValueError(f"Called unwrap on an error value: {self._value}")
        # self._value自体はTまたはE型だが、ここではT型であることが保証されているため、
        # cast()を使ってT型であることを明示し、型チェックを通している
        return cast(T, self._value)

    def unwrap_error(self) -> E:
        """
        失敗時に呼ばれることを前提として、失敗時の値(E型)を返す
        もし成功時(result_ok)の状態で呼ばれた場合、例外(ValueError)を発生させる
        """
        if self._is_ok:
            raise ValueError(
                f"Called unwrap_error on an ok value: {self._value}"
            )
        # unwrap()と同様の理由でcast()を使用して、型チェックを通している
        return cast(E, self._value)

    def __repr__(self) -> str:
        if self._is_ok:
            return f"Result.ok({repr(self._value)})"
        else:
            return f"Result.error({repr(self._value)})"

    @classmethod
    def ok(cls, value: T) -> "Result[T, E]":
        """
        成功時のResultインスタンスを生成
        """
        return cls(value=value, is_ok=True)

    @classmethod
    def error(cls, value: E) -> "Result[T, E]":
        """
        失敗時のResultインスタンスを生成
        """
        return cls(value=value, is_ok=False)
