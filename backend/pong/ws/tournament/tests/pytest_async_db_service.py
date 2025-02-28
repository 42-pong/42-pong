import pytest
import pytest_asyncio
from channels.db import database_sync_to_async  # type: ignore

from tournaments.constants import RoundFields, TournamentFields
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament
from ws.tournament.async_db_service import (
    create_round,
)


@pytest_asyncio.fixture
@database_sync_to_async
def create_tournament() -> Tournament:
    """
    テストの前処理として使用する関数
    非同期フィクスチャ：トーナメントを作成
    """
    tournament = Tournament.objects.create(
        status=TournamentFields.StatusEnum.ON_GOING.value
    )
    return tournament


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_round(create_tournament: Tournament) -> None:
    tournament = create_tournament

    # ラウンドを作成
    result = await create_round(tournament_id=tournament.id, round_number=1)

    # 結果の検証
    assert result.is_ok
    result_value = result.unwrap()
    assert result_value[RoundFields.ID] is not None
    assert result_value[RoundFields.TOURNAMENT_ID] == tournament.id
    assert result_value[RoundFields.ROUND_NUMBER] == 1
    assert (
        result_value[RoundFields.STATUS]
        == RoundFields.StatusEnum.NOT_STARTED.value
    )
