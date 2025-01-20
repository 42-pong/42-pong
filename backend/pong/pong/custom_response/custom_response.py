import dataclasses
from typing import Final

from rest_framework import response

STATUS: Final[str] = "status"
DATA: Final[str] = "data"
ERRORS: Final[str] = "errors"


@dataclasses.dataclass(frozen=True)
class Status:
    OK: str = "ok"
    ERROR: str = "error"


class CustomResponse(response.Response):
    """
    全appでレスポンスの形式を統一するためのクラス

    Args:
        data  : 成功時のレスポンスデータ
        errors: エラー時のエラーメッセージ
        status: ステータスコード

    レスポンスのJSON形式(self.data):
        {
            "status": "ok" | "error",
            "data": {...},
            "errors": {...}
        }

        - status: 必須。300番台までは"ok"、400番台以上は"error"を格納
        - data  : 成功時のみ、返すデータのdictを格納
        - errors: エラー時のみ、エラーメッセージのdictを格納
    """

    # statusのデフォルト値200は継承元を参考
    # https://github.com/django/django/blob/main/django/http/response.py#L111
    def __init__(
        self,
        data: dict | None = None,
        errors: dict | None = None,
        status: int = 200,
    ):
        # 内部で100-599番以外のステータスコードは例外を発生させる
        super().__init__(None, status=status)
        self.status = status
        self.data = {}

        if status < 400:
            # 300番台までの成功レスポンス
            self.data[STATUS] = Status.OK
            self.data[DATA] = data if data else {}
        else:
            # 400番台以上のエラーレスポンス
            self.data[STATUS] = Status.ERROR
            self.data[ERRORS] = errors if errors else {}
