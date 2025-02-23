import logging
from typing import Optional

from asgiref.sync import sync_to_async

from django.db import DatabaseError, transaction
from rest_framework import serializers as drf_serializers

import utils.result
from tournaments import constants

from tournaments.participation import serializers as participation_serializers
from tournaments.tournament import models as tournament_models
from tournaments.tournament import serializers as tournament_serializers

logger = logging.getLogger("django")
CreateTournamentResult = utils.result.Result[dict, dict]


async def create_tournament_with_participation(
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
            tournament: dict = await sync_to_async(
                tournament_serializer.save
            )()

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
            await sync_to_async(participation_serializer.save)()

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
