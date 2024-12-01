from typing import Generic, TypeVar, Union

T = TypeVar("T")  # 成功時の値の型
E = TypeVar("E")  # エラー時の値の型


class Result(Generic[T, E]):
    def __init__(self, value: Union[T, E], is_ok: bool):
        self._value = value
        self._is_ok = is_ok

