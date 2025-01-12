from typing import Any

from rest_framework import serializers

from .. import ws_constants


class BaseWebsocketSerializer(serializers.Serializer):
    """
    Websocketのメッセージスキーマのバリデーションに使うシリアライザ―に継承させるクラス
    """

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        定義したフィールド以外のフィールドが含まれていたら例外を発生させる
        """
        # 許可されていないフィールドがある場合はエラー
        extra_fields = set(self.initial_data.keys()) - set(self.fields.keys())
        if extra_fields:
            raise serializers.ValidationError(
                f"Unexpected fields detected: {', '.join(extra_fields)}"
            )

        return data


class WebsocketInputSerializer(BaseWebsocketSerializer):
    """
    すべてのwebsocketイベントで共通のメッセージスキーマをバリデーションするために使うクラス
    """

    category = serializers.ChoiceField(
        choices=[
            (category.value, category.name)
            for category in ws_constants.Category
        ],
        required=True,
    )
    payload = serializers.JSONField(required=True)  # type: ignore
