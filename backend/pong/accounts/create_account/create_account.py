from typing import Final

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework import serializers as drf_serializers

import utils.result

from .. import constants
from ..player import models, serializers

# 定数
USERNAME_LENGTH: Final[int] = 7

# 関数の結果用のResult型の型エイリアス
SaveUserResult = utils.result.Result[User, dict]
SavePlayerResult = utils.result.Result[models.Player, dict]
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


def _save_user(
    user_serializer: drf_serializers.ModelSerializer,
) -> SaveUserResult:
    """
    引数のSerializerを使い、UserをDBに保存する

    Args:
        user_serializer: UserSerializerのインスタンス

    Returns:
        SaveUserResult: DBに保存されたUserのResult
    """
    if not user_serializer.is_valid():
        return SaveUserResult.error(user_serializer.errors)

    # DBに保存
    user: User = user_serializer.save()
    return SaveUserResult.ok(user)


def _save_player_related_with_user(
    player_data: dict, user_id: int
) -> SavePlayerResult:
    """
    player_dataとUserを紐づけてPlayerSerializerを新規作成し、PlayerをDBに保存する
    app間で共通のPlayerSerializerを使用する

    Args:
        player_data: PlayerSerializerに渡すdata
        user_id: UserのPK

    Returns:
        SavePlayerResult: DBに保存されたPlayerのResult
    """
    # PKであるuser.idを"user"フィールドにセットしUserとPlayerを紐づける
    player_data[constants.PlayerFields.USER] = user_id

    # PlayerSerializer作成
    player_serializer: serializers.PlayerSerializer = (
        serializers.PlayerSerializer(data=player_data)
    )
    if not player_serializer.is_valid():
        return SavePlayerResult.error(player_serializer.errors)

    # DBに保存
    player: models.Player = player_serializer.save()
    return SavePlayerResult.ok(player)


# todo: トランザクションの処理が必要。User,Playerのどちらかが作成されなかった場合はロールバック
def create_account(
    user_serializer: drf_serializers.ModelSerializer, player_data: dict
) -> CreateAccountResult:
    """
    UserとPlayerを新規作成してDBに追加し、作成されたアカウント情報を返す

    Args:
        user_serializer: UserSerializerのインスタンス
        player_data: PlayerSerializerに渡すdata

    Returns:
        CreateAccountResult: 作成されたUserのResult
    """
    # UserSerializerが引数として正しくない場合にassertを発生させる
    _assert_user_serializer(user_serializer)

    # User作成
    save_user_result: SaveUserResult = _save_user(user_serializer)
    if save_user_result.is_error:
        return CreateAccountResult.error(save_user_result.unwrap_error())
    user: User = save_user_result.unwrap()

    # Player作成
    save_player_result: SavePlayerResult = _save_player_related_with_user(
        player_data, user.id
    )
    if save_player_result.is_error:
        return CreateAccountResult.error(save_player_result.unwrap_error())
    # save_player_result.unwrap()でPlayerを取得できるが、使わないため呼ばない

    return CreateAccountResult.ok(user_serializer.data)
