import dataclasses
from typing import Final, Optional

from rest_framework import response

STATUS: Final[str] = "status"
DATA: Final[str] = "data"
CODE: Final[str] = "code"
ERRORS: Final[str] = "errors"


@dataclasses.dataclass(frozen=True)
class Status:
    OK: str = "ok"
    ERROR: str = "error"


@dataclasses.dataclass(frozen=True)
class Code:
    INTERNAL_ERROR: str = "internal_error"
    UNAUTHORIZED: str = "unauthorized"


class CustomResponse(response.Response):
    """
    全appでレスポンスの形式を統一するためのクラス

    Args:
        data  : 成功時のレスポンスデータ
        code  : エラー時のエラーコード(FEでエラーの種類を判別するために定められたコード)
        errors: エラー時のエラーメッセージ(主に開発者向けのエラーメッセージ)
        status: ステータスコード

    レスポンスのJSON形式(self.data):
        {
            "status": "ok" | "error",
            "data": {...},
            "code": ["string", ...],
            "errors": {...}
        }

        - status: 必須。300番台までは"ok"、400番台以上は"error"を格納
        - data  : 成功時のみ、返すデータのdictを格納
        - code  : エラー時のみ、エラーコードのlistを格納
        - errors: エラー時のみ、エラーメッセージのdictを格納
    """

    # statusのデフォルト値200は継承元を参考
    # https://github.com/django/django/blob/main/django/http/response.py#L111
    def __init__(
        self,
        data: Optional[dict] = None,
        code: Optional[list[str]] = None,
        errors: Optional[dict] = None,
        status: int = 200,
    ):
        # 内部で100-599番以外のステータスコードは例外を発生させる
        super().__init__(None, status=status)
        self.status = status
        self.data = {}

        if status < 400:
            # 300番台までの成功レスポンス
            self.data[STATUS] = Status.OK
            self.data[DATA] = data if data is not None else {}
        else:
            # 400番台以上のエラーレスポンス
            self.data[STATUS] = Status.ERROR
            self.data[CODE] = code if code is not None else []
            self.data[ERRORS] = errors if errors is not None else {}
