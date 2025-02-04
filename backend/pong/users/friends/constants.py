import dataclasses


@dataclasses.dataclass(frozen=True)
class FriendshipFields:
    USER_ID: str = "user_id"
    FRIEND_USER_ID: str = "friend_user_id"
