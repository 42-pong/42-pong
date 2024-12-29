from django.contrib.auth.models import User

import utils.result

from . import constants, models, serializers

CreateAccountResult = utils.result.Result[models.Player, dict]


# todo: トランザクションの処理が必要。User,Playerのどちらかが作成されなかった場合はロールバック
def create_account(data: dict) -> CreateAccountResult:
    """
    UserとPlayerを新規作成してDBに追加し、作成されたアカウント情報を返す
    """
    # User作成
    # dataの中にuser情報があるのでpopしてUserSerializerに渡す
    user_data: dict = data.pop(constants.PlayerFields.USER)
    user_serializer: serializers.UserSerializer = serializers.UserSerializer(
        data=user_data
    )
    if not user_serializer.is_valid():
        return CreateAccountResult.error(user_serializer.errors)
    user: User = user_serializer.save()

    # User作成の後にPlayer作成
    player_data: dict = data.copy()
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
