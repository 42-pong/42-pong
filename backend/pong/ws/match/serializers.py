from typing import Any

from rest_framework import serializers

from ..share import constants as ws_constants
from ..share import serializers as ws_serializers
from . import constants as match_constants


class MatchInputINITSerializer(ws_serializers.BaseWebsocketSerializer):
    """
    MATCHイベントのINITステージのメッセージスキーマをバリデーションするために使うクラス
    """

    mode = serializers.ChoiceField(
        choices=[(mode.value, mode.name) for mode in match_constants.Mode],
    )


class MatchInputREADYSerializer(ws_serializers.BaseWebsocketSerializer):
    """
    MATCHイベントのREADYステージのメッセージスキーマをバリデーションするために使うクラス
    """

    pass  # READYステージは空のスキーマ


class MatchInputPLAYSerializer(ws_serializers.BaseWebsocketSerializer):
    """
    MATCHイベントのPLAYステージのメッセージスキーマをバリデーションするために使うクラス
    """

    team = serializers.ChoiceField(
        choices=[(team.value, team.name) for team in match_constants.Team],
    )
    move = serializers.ChoiceField(
        choices=[(move.value, move.name) for move in match_constants.Move],
    )


class MatchInputENDSerializer(ws_serializers.BaseWebsocketSerializer):
    """
    MATCHイベントのENDステージのメッセージスキーマをバリデーションするために使うクラス
    """

    pass  # ENDステージは空のスキーマ


class MatchInputSerializer(ws_serializers.BaseWebsocketSerializer):
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
        choices=[(stage.value, stage.name) for stage in match_constants.Stage]
    )
    data = serializers.JSONField()  # type: ignore

    def validate_data(self, value: dict[str, Any]) -> dict[str, Any]:
        """
        dataフィールドのバリデーションを行うメソッド

        この関数内で例外が投げられても'is_valid()'が必ずcatchする。
        """
        stage: str = self.initial_data[match_constants.Stage.key()]
        data: dict = self.initial_data[ws_constants.DATA_KEY]

        stage_serializer: dict[
            str, type[ws_serializers.BaseWebsocketSerializer]
        ] = {
            match_constants.Stage.INIT.value: MatchInputINITSerializer,
            match_constants.Stage.READY.value: MatchInputREADYSerializer,
            match_constants.Stage.PLAY.value: MatchInputPLAYSerializer,
            match_constants.Stage.END.value: MatchInputENDSerializer,
        }

        serializer_class = stage_serializer.get(stage)
        if serializer_class is None:
            raise serializers.ValidationError(
                f"Invalid stage '{stage}' provided. Expected one of: {', '.join(stage_serializer.keys())}"
            )

        # ステージシリアライザをインスタンス化してバリデーション
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return value
