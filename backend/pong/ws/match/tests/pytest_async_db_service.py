import pytest
import pytest_asyncio
from channels.db import database_sync_to_async  # type: ignore
from django.contrib.auth.models import User

from accounts.player.models import Player
from matches.constants import MatchFields
from matches.match.models import Match
from tournaments.constants import RoundFields, TournamentFields
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament
from ws.match.async_db_service import (
    create_match,
    update_match_status,
)


@database_sync_to_async
def create_tournament_and_round() -> tuple[Tournament, Round]:
    """
    テストの前処理として使用する関数
    トーナメントとラウンドを作成
    """
    tournament = Tournament.objects.create(
        status=TournamentFields.StatusEnum.ON_GOING.value
    )
    round_instance = Round.objects.create(
        tournament=tournament,
        round_number=1,
        status=RoundFields.StatusEnum.NOT_STARTED.value,
    )
    return tournament, round_instance


@database_sync_to_async
def create_user_and_player() -> tuple[User, Player]:
    """
    テストの前処理として使用する関数
    ユーザーとプレーヤーを作成
    """
    user = User.objects.create(
        username="async_test1",
        email="async_test1@example.com",
        password="async_test1_password",
    )
    player = Player.objects.create(user=user)
    return user, player


@pytest_asyncio.fixture
async def tournament_and_round() -> tuple[Tournament, Round]:
    """
    非同期フィクスチャ：トーナメントとラウンドを作成
    """
    return await create_tournament_and_round()


@pytest_asyncio.fixture
async def user_and_player() -> tuple[User, Player]:
    """
    非同期フィクスチャ：ユーザーとプレイヤーを作成
    """
    return await create_user_and_player()


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_match(
    tournament_and_round: tuple[Tournament, Round],
) -> None:
    """
    matchが正常に作成されるかテスト
    """
    tournament, round_instance = tournament_and_round

    # create_matchを呼び出し、round_idを渡す
    round_id = round_instance.id
    result = await create_match(round_id)
    print("result=", result)

    # 結果の検証
    assert result.is_ok
    result_value = result.unwrap()
    assert result_value[MatchFields.ID] is not None
    match = await database_sync_to_async(Match.objects.get)(
        id=result_value[MatchFields.ID]
    )
    assert match.round_id == round_id


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_update_match_status(
    tournament_and_round: tuple[Tournament, Round],
) -> None:
    tournament, round_instance = tournament_and_round

    # 試合を作成
    match = await database_sync_to_async(Match.objects.create)(
        round_id=round_instance.id
    )

    # update_match_statusを呼び出し、試合のステータスを更新
    status = MatchFields.StatusEnum.ON_GOING.value
    result = await update_match_status(match.id, status)

    # 結果の検証
    assert result.is_ok
    result_value = result.unwrap()
    assert result_value[MatchFields.STATUS] == status
    await database_sync_to_async(match.refresh_from_db)()
    assert match.status == status
