from typing import Any

from rest_framework import serializers

from .. import match_enums, ws_constants
from . import ws_serializer


class MatchInputINITSerializer(ws_serializer.BaseWebsocketSerializer):
    """
    MATCHイベントのINITステージのメッセージスキーマをバリデーションするために使うクラス
    """

    mode = serializers.ChoiceField(
        choices=[(mode.value, mode.name) for mode in match_enums.Mode],
        required=True,
    )


class MatchInputREADYSerializer(ws_serializer.BaseWebsocketSerializer):
    """
    MATCHイベントのREADYステージのメッセージスキーマをバリデーションするために使うクラス
    """

    pass  # READYステージは空のスキーマ


class MatchInputPLAYSerializer(ws_serializer.BaseWebsocketSerializer):
    """
    MATCHイベントのPLAYステージのメッセージスキーマをバリデーションするために使うクラス
    """

    team = serializers.ChoiceField(
        choices=[(team.value, team.name) for team in match_enums.Team],
        required=True,
    )
    move = serializers.ChoiceField(
        choices=[(move.value, move.name) for move in match_enums.Move],
        required=True,
    )


class MatchInputENDSerializer(ws_serializer.BaseWebsocketSerializer):
    """
    MATCHイベントのENDステージのメッセージスキーマをバリデーションするために使うクラス
    """

    pass  # ENDステージは空のスキーマ


class MatchInputSerializer(ws_serializer.BaseWebsocketSerializer):
    """
    MATCHイベントで共通のメッセージスキーマをバリデーションするために使うクラス
    Stageごとに各Stageのシリアライザ―に処理を移譲する

    is_valid()
        Return:
            bool: validationが通ればTrue, 通らなければFalse
        Raise:
            raise_exception=Trueであれば、rest_framework.serializers.ValidationErrorを投げる
    """

    stage = serializers.ChoiceField(
        choices=[(stage.value, stage.name) for stage in match_enums.Stage],
        required=True,
    )
    data = serializers.JSONField(required=True)  # type: ignore

    def validate_data(self, value: dict[str, Any]) -> dict[str, Any]:
        """
        dataフィールドのバリデーションを行うメソッド

        この関数内で例外が投げられても'is_valid()'が必ずcatchする。
        """
        stage: str = self.initial_data[match_enums.Stage.key()]
        data: dict = self.initial_data[ws_constants.DATA_KEY]

        serializer_map: dict[
            str, type[ws_serializer.BaseWebsocketSerializer]
        ] = {
            match_enums.Stage.INIT.value: MatchInputINITSerializer,
            match_enums.Stage.READY.value: MatchInputREADYSerializer,
            match_enums.Stage.PLAY.value: MatchInputPLAYSerializer,
            match_enums.Stage.END.value: MatchInputENDSerializer,
        }

        serializer_class = serializer_map.get(stage)
        if not serializer_class:
            raise serializers.ValidationError(
                f"Invalid stage '{stage}' provided. Expected one of: {', '.join(serializer_map.keys())}"
            )

        # ステージシリアライザをインスタンス化してバリデーション
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return value
