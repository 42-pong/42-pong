from rest_framework import serializers

from accounts import constants
from accounts.player import models


class UsersSerializer(serializers.Serializer):
    """
    users app全体で共通のシリアライザ
    Playerとそれに紐づくUserから、返しても良い情報のみをまとめてシリアライズする
    """

    id = serializers.IntegerField(source="user.id")
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    display_name = serializers.CharField()
    # todo: こことfieldにavatar追加

    class Meta:
        model = models.Player
        fields = (
            constants.UserFields.ID,
            constants.UserFields.USERNAME,
            constants.UserFields.EMAIL,
            constants.PlayerFields.DISPLAY_NAME,
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
