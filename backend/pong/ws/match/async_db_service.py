import logging

from channels.db import database_sync_to_async  # type: ignore
from django.contrib.auth.models import User
from django.db import DatabaseError, transaction

import utils.result
from accounts.player import models as player_models
from matches import constants
from matches.match import models as match_models
from matches.participation import models as participation_models
from matches.score import models as score_models

logger = logging.getLogger(__name__)
CreateMatchResult = utils.result.Result[dict, dict]
UpdateMatchResult = utils.result.Result[dict, dict]
CreateParticipationResult = utils.result.Result[dict, dict]
CreateScoreResult = utils.result.Result[dict, dict]
UpdateParticipationResult = utils.result.Result[dict, dict]


@database_sync_to_async
def create_match(round_id: int) -> CreateMatchResult:
    """
    新しい試合を作成する。
    """
    try:
        match = match_models.Match.objects.create(round_id=round_id)
    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return CreateMatchResult.error({"DatabaseError": str(e)})

    return CreateMatchResult.ok({constants.MatchFields.ID: match.id})


@database_sync_to_async
def update_match_status(match_id: int, status: str) -> UpdateMatchResult:
    """
    試合のステータスを更新する。
    """
    try:
        with transaction.atomic():
            match = match_models.Match.objects.get(id=match_id)
            match.status = status
            match.save()
    except match_models.Match.DoesNotExist as e:
        logger.error(f"DoesNotExist: {e}")
        return UpdateMatchResult.error({"DoesNotExist": str(e)})
    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return UpdateMatchResult.error({"DatabaseError": str(e)})
    return UpdateMatchResult.ok(
        {
            constants.MatchFields.ID: match.id,
            constants.MatchFields.STATUS: match.status,
        }
    )


@database_sync_to_async
def create_participation(
    match_id: int, user_id: int, team: str, is_win: bool
) -> CreateParticipationResult:
    """
    試合の参加レコードを作成する。
    """
    try:
        user = User.objects.get(id=user_id)
        player = player_models.Player.objects.get(user=user)
        participation = participation_models.Participation.objects.create(
            match_id=match_id,
            player=player,
            team=team,
            is_win=is_win,
        )
    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return CreateParticipationResult.error({"DatabaseError": str(e)})
    return CreateParticipationResult.ok(
        {
            constants.ParticipationFields.ID: participation.id,
            constants.ParticipationFields.TEAM: participation.team,
        }
    )


@database_sync_to_async
def update_participation_is_win(
    match_id: int, user_id: int
) -> UpdateParticipationResult:
    """
    試合に勝利したプレーヤーのis_winカラムをtrueに更新する
    """
    try:
        with transaction.atomic():
            participation = participation_models.Participation.objects.get(
                match_id=match_id, player__user_id=user_id
            )
            participation.is_win = True
            participation.save()
    except participation_models.Participation.DoesNotExist as e:
        logger.error(f"DoesNotExist: {e}")
        return UpdateParticipationResult.error({"DoesNotExist": str(e)})
    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return UpdateParticipationResult.error({"DatabaseError": str(e)})
    return UpdateParticipationResult.ok(
        {
            "id": participation.id,
            "is_win": participation.is_win,
        }
    )


@database_sync_to_async
def create_score(
    match_id: int, user_id: int, pos_x: int, pos_y: int
) -> CreateScoreResult:
    """
    指定された match_id と user_id に対応する試合参加情報に紐づくスコアを作成する。
    """
    try:
        with transaction.atomic():
            participation = participation_models.Participation.objects.get(
                match_id=match_id, player__user_id=user_id
            )

            score = score_models.Score.objects.create(
                match_participation=participation,
                pos_x=pos_x,
                pos_y=pos_y,
            )
    except participation_models.Participation.DoesNotExist as e:
        logger.error(f"DoesNotExist: {e}")
        return CreateScoreResult.error({"DoesNotExist": str(e)})
    except DatabaseError as e:
        logger.error(f"DatabaseError: {e}")
        return CreateScoreResult.error({"DatabaseError": str(e)})
    return CreateScoreResult.ok(
        {
            constants.ScoreFields.ID: score.id,
            constants.ScoreFields.MATCH_PARTICIPATION_ID: score.match_participation_id,
            constants.ScoreFields.POS_X: score.pos_x,
            constants.ScoreFields.POS_Y: score.pos_y,
        }
    )
