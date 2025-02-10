from rest_framework import serializers

from .. import constants


def invalid_same_user_validator(user_id: int, friend_user_id: int) -> None:
    """
    Friendshipに渡すfriend_user_idが自分自身である場合に例外を発生させる
    create,destroyのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        friend_user_id: フレンド追加対象・削除対象のユーザーのID

    Raises:
        serializers.ValidationError: フレンドとして追加したいユーザーが自分自身の場合
    """
    if user_id == friend_user_id:
        raise serializers.ValidationError(
            {
                constants.FriendshipFields.FRIEND_USER_ID: "The friend_user_id cannot be the same as user_id."
            },
            code="internal_error",  # todo: constantsに置き換え
        )
