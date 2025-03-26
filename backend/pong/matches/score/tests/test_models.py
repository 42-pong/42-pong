from typing import ClassVar
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.player.models import Player
from matches import constants
from matches.match.models import Match
from matches.participation.models import Participation
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament

from ..models import Score


class ScoreModelTest(TestCase):
    user: ClassVar[User]
    player: ClassVar[Player]
    tournament: ClassVar[Tournament]
    round: ClassVar[Round]
    match: ClassVar[Match]

    @classmethod
    def setUpTestData(cls) -> None:
        """
        classで一度だけ初期化される
        """

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value="avatars/test.png",
        )
        def _create_player(
            user: User, mock_identicon: mock.MagicMock
        ) -> Player:
            return Player.objects.create(user=user)

        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )
        cls.player = _create_player(cls.user)
        cls.tournament = Tournament.objects.create()
        cls.round = Round.objects.create(
            tournament=cls.tournament, round_number=1
        )
        cls.match = Match.objects.create(round=cls.round)

    def setUp(self) -> None:
        # ParticipationとScoreを実際に作成
        self.participation = Participation.objects.create(
            match=self.match,
            player=self.player,
            team=constants.ParticipationFields.TeamEnum.ONE.value,
        )

        self.score = Score.objects.create(
            match_participation=self.participation, pos_x=600, pos_y=200
        )

    def test_participation_creation(self) -> None:
        """
        Scoreが正常に作成されているかテスト
        """
        # DBの値を反映
        self.participation.refresh_from_db()
        self.score.refresh_from_db()

        self.assertEqual(self.score.match_participation, self.participation)

    def test_delete_score(self) -> None:
        """
        Scoreを削除しても、紐づくParticipationは削除されないことを確認
        """
        participation_id = self.participation.id
        self.score.delete()

        self.assertFalse(Score.objects.exists())
        self.assertTrue(
            Participation.objects.filter(id=participation_id).exists()
        )

    def test_delete_participation_related_to_score(self) -> None:
        """
        Participationを削除したら、紐づくScoreも削除されることを確認
        """
        self.participation.delete()

        self.assertFalse(Participation.objects.exists())
        self.assertFalse(Score.objects.exists())
