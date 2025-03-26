import dataclasses


@dataclasses.dataclass(frozen=True)
class FriendshipFields:
    ID: str = "id"
    USER_ID: str = "user_id"
    FRIEND_USER_ID: str = "friend_user_id"
    FRIEND: str = "friend"
    CREATED_AT: str = "created_at"
    UPDATED_AT: str = "updated_at"
