import logging
from typing import Optional

from channels.db import database_sync_to_async  # type: ignore
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError, transaction
from rest_framework import serializers as drf_serializers

import utils.result
from accounts.player import models as player_models
from tournaments import constants
from tournaments.participation import models as participation_models
from tournaments.participation import serializers as participation_serializers
from tournaments.tournament import models as tournament_models
from tournaments.tournament import serializers as tournament_serializers

logger = logging.getLogger(__name__)
CreateParticipationResult = utils.result.Result[dict, dict]
CreateTournamentResult = utils.result.Result[dict, dict]
DeleteParticipationResult = utils.result.Result[dict, dict]
UpdateTournamentResult = utils.result.Result[dict, dict]
UpdateParticipationResult = utils.result.Result[dict, dict]


def handle_validation_error(e: drf_serializers.ValidationError) -> dict:
    logger.error(f"ValidationError: {e}")
    if isinstance(e.detail, list):
        return {"ValidationError": e.detail}
    return e.detail


def handle_database_error(e: DatabaseError, custom_message: str) -> dict:
    logger.error(f"DatabaseError: {e}")
    return {"DatabaseError": custom_message}


def handle_does_not_exist_error(
    e: ObjectDoesNotExist, custom_message: str
) -> dict:
    logger.error(f"DoesNotExistError: {e}")
    return {"DoesNotExistError": custom_message}


@database_sync_to_async
def get_player_id_by_user_id(user_id: int) -> Optional[int]:
    """
    user_idからplayer_idを取得する関数

    Args:
        user_id (int): ユーザーのID

    Returns:
        Optional[int]: player_id、見つからない場合はNone
    """
    try:
        player = player_models.Player.objects.get(user_id=user_id)
        return player.id
    except player_models.Player.DoesNotExist as e:
        logger.error(f"DoesNotExist: {e}")
        return None


@database_sync_to_async
def create_participation(
    tournament_id: int, user_id: int, participation_name: str
) -> CreateParticipationResult:
    """
    新しいParticipationインスタンスを作成する関数。

    tournament_id: トーナメントのID
    user_id: プレイヤーのID
    participation_name: プレイヤーの参加名
    """
    try:
        # user_idからplayer_idを取得
        player_id = get_player_id_by_user_id(user_id)
        if player_id is None:
            return CreateParticipationResult.error(
                {"error": "Player not found for the given user_id"}
            )

        # 参加情報を作成
        data = {
            constants.ParticipationFields.TOURNAMENT_ID: tournament_id,
            constants.ParticipationFields.PLAYER_ID: player_id,
            constants.ParticipationFields.PARTICIPATION_NAME: participation_name,
        }

        # シリアライザに渡すデータをバリデーション
        participation_serializer = (
            participation_serializers.ParticipationCommandSerializer(data=data)
        )
        participation_serializer.is_valid(raise_exception=True)

        # バリデーションを通過したデータを元にインスタンスを作成
        participation_serializer.save()

    except drf_serializers.ValidationError as e:
        return CreateParticipationResult.error(handle_validation_error(e))

    except DatabaseError as e:
        return CreateParticipationResult.error(
            handle_database_error(e, "Failed to create participation.")
        )

    return CreateParticipationResult.ok(participation_serializer.data)


@database_sync_to_async
def create_tournament_with_participation(
    user_id: int, participation_name: str
) -> CreateTournamentResult:
    """
    トーナメントと参加情報を一つのトランザクションで作成する関数。

    Args:
        user_id (int): 参加プレイヤーの UserID
        participation_name (str): トーナメント内での表示名

    Returns:
        CreateTournamentResult: 作成されたtournamentのシリアライズ後のデータのResult
          - ok: Tournament,Participationの作成に成功した場合
          - error: ParticipationSerializerに渡すplayer_idかparticipation_nameのValidationError、またはDatabaseError
    """
    try:
        with transaction.atomic():
            # 1. トーナメントを作成
            tournament_serializer = (
                tournament_serializers.TournamentCommandSerializer(data={})
            )
            tournament_serializer.is_valid(raise_exception=True)
            tournament: dict = tournament_serializer.save()

            # 2. 参加情報を作成（create_participation関数を呼び出す）
            participation_result = create_participation(
                tournament_id=tournament[constants.TournamentFields.ID],
                user_id=user_id,
                participation_name=participation_name,
            )
            if participation_result.is_error():
                return CreateTournamentResult.error(
                    participation_result.error()
                )

    except drf_serializers.ValidationError as e:
        return CreateTournamentResult.error(handle_validation_error(e))

    except DatabaseError as e:
        return CreateTournamentResult.error(
            handle_database_error(e, "Failed to create participation.")
        )

    # 使う想定なのはidだけだが、一応dictごとと返す
    return CreateTournamentResult.ok(tournament_serializer.data)


@database_sync_to_async
def get_waiting_tournament() -> Optional[int]:
    """
    募集中のトーナメントクエリセットの中で最初の1件を取得する

    Return:
        int: 正常に取得できた場合
        None: 募集中のトーナメントが一つもない場合
    """
    tournament = tournament_models.Tournament.objects.filter(
        status=constants.TournamentFields.StatusEnum.NOT_STARTED.value
    ).first()

    if tournament is not None:
        return tournament.id

    return None


@database_sync_to_async
def update_tournament_status(
    id: int, new_status: str
) -> UpdateTournamentResult:
    """
    tournamentテーブルの状態を更新するための関数。

    Returns:
        UpdateTournamentResult: 作成されたtournamentのシリアライズ後のデータのResult
          - ok: Tournamentのstatus更新に成功した場合
          - error: TournamentSerializerに渡すstatusが存在しないか、存在しても他の条件により不正な場合のValidationError、またはDatabaseError
    """
    try:
        # 他の操作が間に入り込むこともありそうなのでトランザクションで一応かこっている。
        with transaction.atomic():
            tournament = tournament_models.Tournament.objects.aget(id=id)
            data = {
                constants.TournamentFields.STATUS: new_status,
            }

            serializer = tournament_serializers.TournamentCommandSerializer(
                instance=tournament, data=data
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

    except drf_serializers.ValidationError as e:
        return UpdateTournamentResult.error(handle_validation_error(e))

    except tournament_models.Tournament.DoesNotExist as e:
        return UpdateTournamentResult.error(
            handle_does_not_exist_error(
                e, "Tournament object does not exists."
            )
        )

    except DatabaseError as e:
        return UpdateTournamentResult.error(
            handle_database_error(e, "Failed to update tournament.")
        )

    return UpdateTournamentResult.ok(serializer.data)


@database_sync_to_async
def update_participation_ranking(
    tournament_id: int, user_id: int, ranking: int
) -> UpdateParticipationResult:
    """
    大会終了時にtournament_participationsテーブルのランキングを更新

    Returns:
        UpdateTournamentResult: 作成されたtournamentのシリアライズ後のデータのResult
          - ok: Participationのranking更新に成功した場合
          - error: rankingの値が不正な場合のValidationError、またはDatabaseError
    """

    try:
        with transaction.atomic():
            participation = participation_models.Participation.objects.select_for_update().get(
                tournament_id=tournament_id,
                player__user_id=user_id,  # ここで逆引き
            )

            # シリアライザーを使ってバリデーション & 更新
            serializer = (
                participation_serializers.ParticipationCommandSerializer(
                    participation,
                    data={constants.ParticipationFields.RANKING: ranking},
                    partial=True,
                )
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

    except drf_serializers.ValidationError as e:
        return UpdateParticipationResult.error(handle_validation_error(e))

    except DatabaseError as e:
        return UpdateParticipationResult.error(
            handle_database_error(e, "Failed to update participation.")
        )

    except participation_models.Participation.DoesNotExist as e:
        return UpdateParticipationResult.error(
            handle_does_not_exist_error(
                e, "Participatin object does not exists."
            )
        )

    return UpdateParticipationResult.ok(serializer.data)


@database_sync_to_async
def delete_participation(
    tournament_id: int, user_id: int
) -> DeleteParticipationResult:
    """
    トーナメントとプレイヤーに基づいて参加情報を削除する関数。

    Args:
        tournament_id (int): トーナメントの ID
        user_id (int): Userの ID

    Returns:
        UpdateParticipationResult: 参加情報削除の結果
          - ok: 参加情報の削除に成功した場合
          - error: 指定されたトーナメントとプレイヤーの組み合わせが存在しない場合や、削除処理中のエラー
    """
    try:
        with transaction.atomic():
            # 参加情報を取得して削除
            participation = participation_models.Participation.objects.get(
                tournament_id=tournament_id, player__user_id=user_id
            )
            participation.delete()

    except participation_models.Participation.DoesNotExist as e:
        return DeleteParticipationResult.error(
            handle_does_not_exist_error(
                e, "Participatin object does not exists."
            )
        )

    except DatabaseError as e:
        return DeleteParticipationResult.error(
            handle_database_error(e, "Failed to delete participation.")
        )

    return DeleteParticipationResult.ok(
        {"message": "Participation deleted successfully."}
    )
