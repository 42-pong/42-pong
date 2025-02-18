import dataclasses


@dataclasses.dataclass(frozen=True)
class BlockRelationshipFields:
    USER_ID: str = "user_id"
    BLOCKED_USER_ID: str = "blocked_user_id"
