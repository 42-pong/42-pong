from typing import Final

from django.contrib.auth.models import User
from django.db import DatabaseError, transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers as drf_serializers

import utils.result

from .. import constants
from ..player import models, serializers

# 定数
USERNAME_LENGTH: Final[int] = 7

# 関数の結果用のResult型の型エイリアス
CreateAccountResult = utils.result.Result[dict, dict]


def get_unique_random_username() -> str:
    """
    ユニークかつランダムな文字列のusernameを生成する
    UserModelのusernameとして使用する
    ランダム文字列は英子文字・英大文字・数字の計62文字の組み合わせ

    Returns:
        str: ランダム文字列かつ、DBに存在しないusername
    """
    while True:
        random_str: str = get_random_string(length=USERNAME_LENGTH)
        if not User.objects.filter(username=random_str).exists():
            break
    return random_str


# todo: 以下の関数は全てcreate_account()内でのみ使われる想定のため、まとめてクラス化すると良さそう
def _assert_user_serializer(
    user_serializer: drf_serializers.ModelSerializer,
) -> None:
    """
    ModelSerializerを継承したSerializerの検証を行う
    実装上UserModelに対応していることを想定しているため、満たしていない場合はAssertionError

    Args:
        user_serializer: UserModelに対応している、ModelSerializerを継承したSerializerのインスタンス

    Raises:
        AssertionError: UserModelに対応していない場合
    """
    # Meta.modelが存在しUserであれば、UserModelに対応しているserializerと判定する
    if (
        not hasattr(user_serializer, "Meta")
        or not hasattr(user_serializer.Meta, "model")
        or user_serializer.Meta.model is not User
    ):
        raise AssertionError(
            "UserSerializer should be a ModelSerializer for User model"
        )


def _save_user(user_serializer: drf_serializers.ModelSerializer) -> User:
    """
    引数のSerializerを使い、UserをDBに保存する

    Args:
        user_serializer: UserのSerializerのインスタンス

    Returns:
        User: DBに保存されたUser

    Raises:
        drf_serializers.ValidationError: Serializerのデータが不正な場合
        DatabaseError: DBへの保存に失敗した場合
    """
    user_serializer.is_valid(raise_exception=True)
    # DBに保存
    user: User = user_serializer.save()
    return user


def _save_player(player_data: dict, user_id: int) -> models.Player:
    """
    player_dataとUserを紐づけてPlayerSerializerを新規作成し、PlayerをDBに保存する
    app間で共通のPlayerSerializerを使用する

    Args:
        player_data: PlayerSerializerに渡すdata
        user_id: UserのPK

    Returns:
        Player: DBに保存されたPlayer

    Raises:
        drf_serializers.ValidationError: Serializerのデータが不正な場合
        DatabaseError: DBへの保存に失敗した場合
    """
    # PKであるuser.idを"user"フィールドにセットしUserとPlayerを紐づける
    player_data[constants.PlayerFields.USER] = user_id

    # PlayerSerializer作成
    player_serializer: serializers.PlayerSerializer = (
        serializers.PlayerSerializer(data=player_data)
    )
    player_serializer.is_valid(raise_exception=True)
    # DBに保存
    player: models.Player = player_serializer.save()
    return player


def create_account(
    user_serializer: drf_serializers.ModelSerializer, player_data: dict
) -> CreateAccountResult:
    """
    UserとPlayerを新規作成してDBに追加し、作成されたアカウント情報を返す

    Args:
        user_serializer: UserSerializerのインスタンス
        player_data: PlayerSerializerに渡すdata

    Returns:
        CreateAccountResult: 作成されたUserのシリアライズ後のデータのResult
    """
    # UserSerializerが引数として正しくない場合にassertを発生させる
    _assert_user_serializer(user_serializer)

    try:
        with transaction.atomic():
            user: User = _save_user(user_serializer)
            _save_player(player_data, user.id)
    except drf_serializers.ValidationError as e:
        # e.detail: list or dictのためmypy用にlistの処理も書いているが、ほぼdictだと思われる
        if isinstance(e.detail, list):
            return CreateAccountResult.error({"ValidationError": e.detail})
        return CreateAccountResult.error(e.detail)
    except DatabaseError as e:
        return CreateAccountResult.error(
            {"DatabaseError": f"Failed to create account. Details: {str(e)}."}
        )

    return CreateAccountResult.ok(user_serializer.data)
