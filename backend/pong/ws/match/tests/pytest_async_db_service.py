import pytest
import pytest_asyncio
from channels.db import database_sync_to_async  # type: ignore
from django.contrib.auth.models import User

from accounts.player.models import Player
from tournaments.constants import RoundFields, TournamentFields
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament


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
