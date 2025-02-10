from rest_framework import serializers

from .. import constants, models


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


def is_friendship_exists(user_id: int, friend_user_id: int) -> bool:
    """
    user_idが既にfriend_user_idをフレンドに追加済みであるかどうかを返す
    create,destroyのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        friend_user_id: フレンド追加対象・削除対象のユーザーのID

    Returns:
        bool: 2人が既にフレンドであればTrue、そうでなければFalse

    Raises:
        serializers.ValidationError: フレンドに追加したいidがDBに存在せず、フレンドかどうかの判定ができない場合
    """
    # 既にフレンドであるかどうか
    return models.Friendship.objects.filter(
        user_id=user_id, friend_id=friend_user_id
    ).exists()
