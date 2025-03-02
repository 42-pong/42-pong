import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class PlayerData:
    channel_name: str
    # ローカルマッチでは登録しない
    user_id: Optional[int]
    participation_name: Optional[int]
