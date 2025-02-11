import dataclasses
from typing import Final

from pong.custom_response import custom_response


@dataclasses.dataclass(frozen=True)
class Code:
    INVALID: Final[str] = "invalid"
    INTERNAL_ERROR: Final[str] = custom_response.Code.INTERNAL_ERROR
