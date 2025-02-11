from rest_framework import serializers

from accounts import constants
from accounts.player import models
from accounts.player import serializers as player_serializers


class UsersSerializer(serializers.Serializer):
    """
    users app全体で共通のシリアライザ
    Playerとそれに紐づくUserから、返しても良い情報のみをまとめてシリアライズする
    """

    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    # todo: 別のserializerをネストする方法で他に良い書き方があれば変更する
    display_name = player_serializers.PlayerSerializer().fields[
        constants.PlayerFields.DISPLAY_NAME
    ]
    avatar = player_serializers.PlayerSerializer().fields[
        constants.PlayerFields.AVATAR
    ]

    class Meta:
        model = models.Player
        fields = (
            constants.UserFields.ID,
            constants.UserFields.USERNAME,
            constants.UserFields.EMAIL,
            constants.PlayerFields.DISPLAY_NAME,
            constants.PlayerFields.AVATAR,
        )

    # args,kwargsは型ヒントが複雑かつそのままsuper()に渡したいためignoreで対処
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        # fieldを動的に変更するための引数を取得
        fields: tuple[str] | None = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            # 取得したfields以外をfieldから削除
            allowed: set[str] = set(fields)
            existing: set[str] = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def update(
        self, player: models.Player, validated_data: dict
    ) -> models.Player:
        """
        Playerインスタンスを更新するupdate()のオーバーライド
        """
        player.display_name = validated_data.get(
            constants.PlayerFields.DISPLAY_NAME, player.display_name
        )
        # todo: avatarも新しいものを代入・save()のupdate_fieldsにも追加

        # create()をオーバーライドしない場合、update()内でsave()は必須
        player.save(update_fields=[constants.PlayerFields.DISPLAY_NAME])
        return player
