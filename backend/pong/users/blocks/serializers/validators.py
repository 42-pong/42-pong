from rest_framework import serializers

from accounts.player import models as players_models
from users import constants as users_constants

from .. import constants, models


def invalid_same_user_validator(user_id: int, block_user_id: int) -> None:
    """
    BlockRelationshipに渡すblock_user_idが自分自身である場合に例外を発生させる
    create,destroyのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        block_user_id: ブロック追加対象・削除対象のユーザーのID

    Raises:
        serializers.ValidationError: ブロック追加・削除したいユーザーが自分自身の場合
    """
    if user_id == block_user_id:
        raise serializers.ValidationError(
            {
                constants.BlockRelationshipFields.BLOCKED_USER_ID: "The blocked_user_id cannot be the same as user_id."
            },
            code=users_constants.Code.INTERNAL_ERROR,
        )


def _is_block_relationship_exists(user_id: int, block_user_id: int) -> bool:
    """
    user_idがblock_user_idをブロック済みであるかどうかを返す

    Args:
        user_id: リクエストを送信したユーザーのID
        block_user_id: ブロック追加対象・削除対象のユーザーのID

    Returns:
        bool: user_idがblock_user_idを既にブロックしていればTrue、そうでなければFalse

    Raises:
        serializers.ValidationError: ブロックしたいidがDBに存在せず、ブロック済みかどうかの判定ができない場合
    """
    # ブロックに追加したいidのPlayerがDBに存在しない場合はエラー
    if not players_models.Player.objects.filter(
        user_id=block_user_id
    ).exists():
        raise serializers.ValidationError(
            {
                constants.BlockRelationshipFields.BLOCKED_USER_ID: "The user does not exist."
            },
            code=users_constants.Code.NOT_EXISTS,
        )
    # ブロック済みであるかどうか
    return models.BlockRelationship.objects.filter(
        user_id=user_id, blocked_user_id=block_user_id
    ).exists()


def already_block_validator(user_id: int, block_user_id: int) -> None:
    """
    user_idがblock_user_idをブロック済みである場合に例外を発生させる
    createのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        block_user_id: ブロック対象のユーザーのID

    Raises:
        serializers.ValidationError: ブロックしたいユーザーがブロック済みである場合
    """
    if _is_block_relationship_exists(user_id, block_user_id):
        raise serializers.ValidationError(
            {
                constants.BlockRelationshipFields.BLOCKED_USER_ID: "The user is already blocked."
            },
            code=users_constants.Code.INVALID,
        )


def not_block_validator(user_id: int, block_user_id: int) -> None:
    """
    user_idがblock_user_idをブロックしていない場合に例外を発生させる
    destroyのserializerのvalidate()で呼ばれる想定

    Args:
        user_id: リクエストを送信したユーザーのID
        block_user_id: ブロック解除対象のユーザーのID

    Raises:
        serializers.ValidationError: ブロック解除したいユーザーをブロックしていない場合
    """
    if not _is_block_relationship_exists(user_id, block_user_id):
        raise serializers.ValidationError(
            {
                constants.BlockRelationshipFields.BLOCKED_USER_ID: "The user is not blocked."
            },
            code=users_constants.Code.INVALID,
        )
