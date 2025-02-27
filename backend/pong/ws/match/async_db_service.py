import logging

from channels.db import database_sync_to_async  # type: ignore
from django.db import DatabaseError, transaction

import utils.result
from matches import constants
from matches.match import models as match_models

logger = logging.getLogger(__name__)
CreateMatchResult = utils.result.Result[dict, dict]
UpdateMatchResult = utils.result.Result[dict, dict]


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
