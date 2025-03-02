import os

from django.contrib.auth.models import User
from django.core.files import File
from django.core.validators import RegexValidator
from rest_framework import serializers

from .. import constants
from . import models


def validate_avatar_extension(avatar: File) -> None:
    """
    avatarの拡張子に制限をかけるバリデータ
    extensionが空文字列の場合はImageFeildのバリデータで先にエラーになるためここではチェックしない
    """
    valid_extensions: set[str] = {".png", ".jpg", ".jpeg", ".gif"}
    # mypyにavatar.nameがNoneの可能性を指摘されるが、ImageFieldのvalidatorでextensionがあることは確認済みのため無視
    _, extension = os.path.splitext(avatar.name)  # type: ignore[type-var]
    # is Noneも確認しないとmypyのエラーになるので念のため追加
    if extension is None:
        raise serializers.ValidationError("Must contain a file extension.")
    if extension.lower() not in valid_extensions:
        raise serializers.ValidationError(
            f"Unsupported file extension: {extension}. "
            f"Supported extensions are {", ".join(valid_extensions)}."
        )


class PlayerSerializer(serializers.ModelSerializer):
    """
    Playerモデルのシリアライザ
    Playerモデルの作成・バリデーションを行う
    """

    # 変数名と同じ名前をfieldsに指定する必要がある

    # PrimaryKeyRelatedField: 紐づくターゲットをそのPKを使用して表現する
    user: serializers.PrimaryKeyRelatedField[User] = (
        serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    )
    # display_nameが渡されなかった場合、"default"という文字列をデフォルト値として設定する
    display_name: serializers.CharField = serializers.CharField(
        max_length=15,
        default="default",
        validators=[
            # 使用可能文字列を指定: 英子文字・英大文字・数字・記号(-_.~)
            RegexValidator(
                regex=r"^[a-zA-Z0-9-_.~]+$",
                message="Must contain only alphanumeric characters or some symbols(-_.~)",
            )
        ],
    )
    avatar: serializers.ImageField = serializers.ImageField(
        required=False,
        allow_null=True,
        max_length=constants.MAX_AVATAR_FILE_NAME_LENGTH,  # 画像ファイル名の長さ
        validators=[validate_avatar_extension],
    )

    class Meta:
        model = models.Player
        fields = (
            constants.PlayerFields.USER,
            constants.PlayerFields.DISPLAY_NAME,
            constants.PlayerFields.AVATAR,
        )
