import logging
from typing import Optional

from channels.db import database_sync_to_async  # type: ignore
from django.db import DatabaseError, transaction
from rest_framework import serializers as drf_serializers

import utils.result
from tournaments import constants
from tournaments.participation import models as participation_models
from tournaments.participation import serializers as participation_serializers
from tournaments.tournament import models as tournament_models
from tournaments.tournament import serializers as tournament_serializers

logger = logging.getLogger(__name__)
CreateTournamentResult = utils.result.Result[dict, dict]
UpdateTournamentResult = utils.result.Result[dict, dict]
UpdateParticipationResult = utils.result.Result[dict, dict]


@database_sync_to_async
def create_tournament_with_participation(
    player_id: int, participation_name: str
) -> CreateTournamentResult:
    """
    トーナメントと参加情報を一つのトランザクションで作成する関数。

    Args:
        player_id (int): 参加プレイヤーの ID
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

            # 2. 参加情報を作成
            participation_data = {
                constants.ParticipationFields.TOURNAMENT_ID: tournament[
                    constants.TournamentFields.ID
                ],
                constants.ParticipationFields.PLAYER_ID: player_id,
                constants.ParticipationFields.PARTICIPATION_NAME: participation_name,
            }
            participation_serializer = (
                participation_serializers.ParticipationCommandSerializer(
                    data=participation_data
                )
            )
            participation_serializer.is_valid(raise_exception=True)
            participation_serializer.save()

    except drf_serializers.ValidationError as e:
        logger.error(f"VaridationError: {e}")
        if isinstance(e.detail, list):
            return CreateTournamentResult.error({"ValidationError": e.detail})
        return CreateTournamentResult.error(e.detail)

    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return CreateTournamentResult.error(
            {"DatabaseError": f"Failed to create account. Details: {str(e)}."}
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
        logger.error(f"VaridationError: {e}")
        if isinstance(e.detail, list):
            return UpdateTournamentResult.error({"ValidationError": e.detail})
        return UpdateTournamentResult.error(e.detail)

    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return UpdateTournamentResult.error(
            {"DatabaseError": f"Failed to create account. Details: {str(e)}."}
        )

    return UpdateTournamentResult.ok(serializer.data)


@database_sync_to_async
def update_participation_ranking(
    tournament_id: int, user_id: int, ranking: int
) -> UpdateParticipationResult:
    """
    大会終了時にtournament_participationsテーブルのランキングを更新

    同じプレーヤーが同じトーナメントに参加することはないため、同時にトーナメント参加レコードに対して更新処理をすることはない。よってここではトランザクションで処理をまとめていない。

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
        logger.error(f"VaridationError: {e}")
        if isinstance(e.detail, list):
            return UpdateParticipationResult.error(
                {"ValidationError": e.detail}
            )
        return UpdateParticipationResult.error(e.detail)

    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return UpdateParticipationResult.error(
            {"DatabaseError": f"Failed to create account. Details: {str(e)}."}
        )

    return UpdateParticipationResult.ok(serializer.data)
