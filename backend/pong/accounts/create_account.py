from django.contrib.auth.models import User
from rest_framework import serializers as def_serializers

import utils.result

from . import constants, models, serializers

CreateAccountResult = utils.result.Result[models.Player, dict]


# todo: トランザクションの処理が必要。User,Playerのどちらかが作成されなかった場合はロールバック
def create_account(
    user_serializer: def_serializers.ModelSerializer, player_data: dict
) -> CreateAccountResult:
    """
    UserとPlayerを新規作成してDBに追加し、作成されたアカウント情報を返す

    Args:
        user_serializer: UserSerializerのインスタンス
        player_data: PlayerSerializerに渡すdata
    """
    # User作成
    user: User = user_serializer.save()

    # User作成の後にPlayer作成
    # PKであるuser.idを"user"フィールドにセットしUserとPlayerを紐づける
    player_data[constants.PlayerFields.USER] = user.id
    player_serializer: serializers.PlayerSerializer = (
        serializers.PlayerSerializer(data=player_data)
    )
    if not player_serializer.is_valid():
        return CreateAccountResult.error(player_serializer.errors)
    player: models.Player = player_serializer.save()
    # todo: userを返すか、accountクラスなどに詰めて返す
    return CreateAccountResult.ok(player)
