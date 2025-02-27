from typing import Final
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from accounts import constants as accounts_constants
from accounts.player import models as player_models
from matches import constants as matches_constants
from matches.match import models as match_models
from matches.participation import models as participation_models
from tournaments.round import models as round_models
from tournaments.tournament import models as tournament_models
from users.friends import constants as friends_constants

from ... import constants, serializers

USERNAME: Final[str] = accounts_constants.UserFields.USERNAME
EMAIL: Final[str] = accounts_constants.UserFields.EMAIL
PASSWORD: Final[str] = accounts_constants.UserFields.PASSWORD
USER: Final[str] = accounts_constants.PlayerFields.USER
DISPLAY_NAME: Final[str] = accounts_constants.PlayerFields.DISPLAY_NAME
MATCH_WINS: Final[str] = constants.UsersFields.MATCH_WINS
MATCH_LOSSES: Final[str] = constants.UsersFields.MATCH_LOSSES

USER_ID: Final[str] = friends_constants.FriendshipFields.USER_ID

MOCK_AVATAR_NAME: Final[str] = "avatars/sample.png"


class UsersSerializerTests(TestCase):
    def setUp(self) -> None:
        """
        TestCaseのsetUpメソッドのオーバーライド
        1つのUserと、そのUserに紐づく1つのPlayerをDBに保存
        """

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value=MOCK_AVATAR_NAME,
        )
        def _create_user_and_related_player(
            user_data: dict, player_data: dict, mock_identicon: mock.MagicMock
        ) -> tuple[User, player_models.Player]:
            user: User = User.objects.create_user(**user_data)
            player_data[USER] = user
            player: player_models.Player = player_models.Player.objects.create(
                **player_data
            )
            return user, player

        self.user_data: dict = {
            USERNAME: "testuser_1",
            EMAIL: "testuser_1@example.com",
            PASSWORD: "testpassword",
        }
        self.player_data: dict = {DISPLAY_NAME: "display_name1"}
        self.user, self.player = _create_user_and_related_player(
            self.user_data, self.player_data
        )

        # tournament1つ作成
        self.tournament: tournament_models.Tournament = (
            tournament_models.Tournament.objects.create()
        )
        # round3つ・match3つ・participation3つを作成
        self.participation_list: list[participation_models.Participation] = []
        for i in range(1, 4):
            round: round_models.Round = round_models.Round.objects.create(
                tournament=self.tournament, round_number=i
            )
            match: match_models.Match = match_models.Match.objects.create(
                round=round
            )
            participation: participation_models.Participation = (
                participation_models.Participation.objects.create(
                    match=match, player=self.player, team="1"
                )
            )
            self.participation_list.append(participation)

    def test_field_match_wins(self) -> None:
        """
        勝利した試合の数が正しく取得できることを確認
        """
        # 3つの内2つのmatchに勝利
        for participation in self.participation_list[:2]:
            participation.is_win = True
            participation.save()
        # user1をログインユーザーとしてserializer作成
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player,
            context={USER_ID: self.user.id},
        )

        # 勝利した試合の数が2であることを確認
        self.assertEqual(serializer.data[MATCH_WINS], 2)
        # 負けたCOMPLETEDな試合の数が0であることを確認
        self.assertEqual(serializer.data[MATCH_LOSSES], 0)

    def test_field_match_losses(self) -> None:
        """
        敗北した試合の数が正しく取得できることを確認
        """
        # is_win==Falseの3つのmatchの内、2つのmatchのstatusをCOMPLETEDに変更
        for participation in self.participation_list[:2]:
            participation.match.status = (
                matches_constants.MatchFields.StatusEnum.COMPLETED.value
            )
            participation.match.save()
        # user1をログインユーザーとしてserializer作成
        serializer: serializers.UsersSerializer = serializers.UsersSerializer(
            self.player,
            context={USER_ID: self.user.id},
        )

        # 敗北した試合の数がis_win==FalseかつCOMPLETEDの2であることを確認
        self.assertEqual(serializer.data[MATCH_LOSSES], 2)
