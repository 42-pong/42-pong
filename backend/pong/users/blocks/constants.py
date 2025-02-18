import dataclasses


@dataclasses.dataclass(frozen=True)
class BlockRelationshipFields:
    ID: str = "id"
    USER_ID: str = "user_id"
    BLOCKED_USER_ID: str = "blocked_user_id"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
