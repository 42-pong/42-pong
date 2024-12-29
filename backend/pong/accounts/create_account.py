from django.contrib.auth.models import User
from rest_framework import serializers as def_serializers

import utils.result

from . import constants, serializers

CreatePlayerSerializerResult = utils.result.Result[
    serializers.PlayerSerializer, dict
]
CreateAccountResult = utils.result.Result[User, dict]


def _create_user_related_player_serializer(
    player_data: dict, user_id: int
) -> CreatePlayerSerializerResult:
    """
    player_dataとUserを紐づけ、PlayerSerializerを新規作成する

    Args:
        user_id: UserのPK
        player_data: PlayerSerializerに渡すdata

    Returns:
        CreatePlayerSerializerResult: PlayerSerializerのResult
    """
    # PKであるuser.idを"user"フィールドにセットしUserとPlayerを紐づける
    player_data[constants.PlayerFields.USER] = user_id

    # PlayerSerializer作成
    player_serializer: serializers.PlayerSerializer = (
        serializers.PlayerSerializer(data=player_data)
    )
    if not player_serializer.is_valid():
        return CreatePlayerSerializerResult.error(player_serializer.errors)
    return CreatePlayerSerializerResult.ok(player_serializer)


# todo: トランザクションの処理が必要。User,Playerのどちらかが作成されなかった場合はロールバック
def create_account(
    user_serializer: def_serializers.ModelSerializer, player_data: dict
) -> CreateAccountResult:
    """
    UserとPlayerを新規作成してDBに追加し、作成されたアカウント情報を返す

    Args:
        user_serializer: UserSerializerのインスタンス
        player_data: PlayerSerializerに渡すdata

    Returns:
        CreateAccountResult: 作成されたUserのResult
    """
    # User作成
    user: User = user_serializer.save()

    # app間で共通のPlayerSerializer作成
    player_serializer_result: CreatePlayerSerializerResult = (
        _create_user_related_player_serializer(player_data, user.id)
    )
    if player_serializer_result.is_error:
        return CreateAccountResult.error(
            player_serializer_result.unwrap_error()
        )
    player_serializer: serializers.PlayerSerializer = (
        player_serializer_result.unwrap()
    )

    # User作成の後にPlayer作成
    player_serializer.save()

    return CreateAccountResult.ok(user)
