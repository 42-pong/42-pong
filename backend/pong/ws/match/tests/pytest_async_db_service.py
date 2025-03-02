from unittest import mock

import pytest
import pytest_asyncio
from channels.db import database_sync_to_async  # type: ignore
from django.contrib.auth.models import User

from accounts.player.models import Player
from matches.constants import MatchFields, ParticipationFields, ScoreFields
from matches.match.models import Match
from matches.participation.models import Participation
from tournaments.constants import RoundFields, TournamentFields
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament
from ws.match.async_db_service import (
    create_match,
    create_participation,
    create_score,
    update_match_status,
    update_participation_is_win,
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


@mock.patch(
    "accounts.player.identicon.generate_identicon",
    return_value="avatars/sample.png",
)
@database_sync_to_async
def create_user_and_player(
    mock_identicon: mock.MagicMock,
) -> tuple[User, Player]:
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


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_participation(
    tournament_and_round: tuple[Tournament, Round],
    user_and_player: tuple[User, Player],
) -> None:
    tournament, round_instance = tournament_and_round
    user, player = user_and_player

    # 試合を作成
    match = await database_sync_to_async(Match.objects.create)(
        round_id=round_instance.id
    )

    # create_participationを呼び出し、参加者を追加
    team = ParticipationFields.TeamEnum.ONE.value
    is_win = True
    result = await create_participation(match.id, user.id, team, is_win)

    # 結果の検証
    assert result.is_ok
    result_value = result.unwrap()
    assert result_value[ParticipationFields.ID] is not None
    participation = await database_sync_to_async(Participation.objects.get)(
        id=result_value[ParticipationFields.ID]
    )
    assert participation.team == team
    assert participation.is_win == is_win


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_update_participation_is_win(
    tournament_and_round: tuple[Tournament, Round],
    user_and_player: tuple[User, Player],
) -> None:
    tournament, round_instance = tournament_and_round
    user, player = user_and_player

    # 試合を作成
    match = await database_sync_to_async(Match.objects.create)(
        round_id=round_instance.id
    )

    # 参加者を作成
    team = ParticipationFields.TeamEnum.ONE.value
    participation = await database_sync_to_async(Participation.objects.create)(
        match_id=match.id, player=player, team=team, is_win=False
    )

    # update_participation_is_winを呼び出し、勝利ステータスを更新
    result = await update_participation_is_win(match.id, user.id)

    # 結果の検証
    assert result.is_ok
    result_value = result.unwrap()
    assert result_value[ParticipationFields.IS_WIN] is True
    await database_sync_to_async(participation.refresh_from_db)()
    assert participation.is_win is True
    assert participation.team is team


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_score(
    tournament_and_round: tuple[Tournament, Round],
    user_and_player: tuple[User, Player],
) -> None:
    tournament, round_instance = tournament_and_round
    user, player = user_and_player

    # 試合を作成
    match = await database_sync_to_async(Match.objects.create)(
        round_id=round_instance.id
    )

    # 参加者を作成
    team = ParticipationFields.TeamEnum.TWO.value
    participation = await database_sync_to_async(Participation.objects.create)(
        match_id=match.id, player=player, team=team, is_win=False
    )

    # create_scoreを呼び出し、スコアを作成
    pos_x = 0
    pos_y = 120
    result = await create_score(match.id, user.id, pos_x, pos_y)

    # 結果の検証
    assert result.is_ok
    result_value = result.unwrap()
    assert result_value[ScoreFields.ID] is not None
    assert result_value[ScoreFields.MATCH_PARTICIPATION_ID] == participation.id
    assert result_value[ScoreFields.POS_X] == 0
    assert result_value[ScoreFields.POS_Y] == 120
