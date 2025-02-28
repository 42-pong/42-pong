from rest_framework import serializers

from accounts.player import models as players_models
from users import constants as users_constants

from .. import constants, models


def invalid_same_user_validator(user_id: int, friend_user_id: int) -> None:
    """
    Friendshipに渡すfriend_user_idが自分自身である場合に例外を発生させる
    create,destroyのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        friend_user_id: フレンド追加対象・削除対象のユーザーのID

    Raises:
        serializers.ValidationError: フレンドとして追加・削除したいユーザーが自分自身の場合
    """
    if user_id == friend_user_id:
        raise serializers.ValidationError(
            {
                constants.FriendshipFields.FRIEND_USER_ID: "The friend_user_id cannot be the same as user_id."
            },
            code=users_constants.Code.INTERNAL_ERROR,
        )


def _is_friendship_exists(user_id: int, friend_user_id: int) -> bool:
    """
    user_idが既にfriend_user_idをフレンドに追加済みであるかどうかを返す

    Args:
        user_id: リクエストを送信したユーザーのID
        friend_user_id: フレンド追加対象・削除対象のユーザーのID

    Returns:
        bool: 2人が既にフレンドであればTrue、そうでなければFalse

    Raises:
        serializers.ValidationError: フレンドに追加したいidがDBに存在せず、フレンドかどうかの判定ができない場合
    """
    # フレンドに追加したいidのPlayerがDBに存在しない場合はエラー
    if not players_models.Player.objects.filter(
        user_id=friend_user_id
    ).exists():
        raise serializers.ValidationError(
            {
                constants.FriendshipFields.FRIEND_USER_ID: "The user does not exist."
            },
            code=users_constants.Code.NOT_EXISTS,
        )
    # 既にフレンドであるかどうか
    return models.Friendship.objects.filter(
        user_id=user_id, friend_id=friend_user_id
    ).exists()


def already_friend_validator(user_id: int, friend_user_id: int) -> None:
    """
    user_idがfriend_user_idを既にフレンド追加済みである場合に例外を発生させる
    createのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        friend_user_id: フレンド追加対象のユーザーのID

    Raises:
        serializers.ValidationError: フレンドとして追加したいユーザーが既にフレンドである場合
    """
    if _is_friendship_exists(user_id, friend_user_id):
        raise serializers.ValidationError(
            {
                constants.FriendshipFields.FRIEND_USER_ID: "The user is already a friend."
            },
            code=users_constants.Code.INVALID,
        )


def not_friend_validator(user_id: int, friend_user_id: int) -> None:
    """
    user_idがfriend_user_idをフレンドに追加していない場合に例外を発生させる
    destroyのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        friend_user_id: フレンド削除対象のユーザーのID

    Raises:
        serializers.ValidationError: フレンドとして削除したいユーザーがフレンドでない場合
    """
    if not _is_friendship_exists(user_id, friend_user_id):
        raise serializers.ValidationError(
            {
                constants.FriendshipFields.FRIEND_USER_ID: "The user is not a friend."
            },
            code=users_constants.Code.INVALID,
        )
