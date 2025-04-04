from typing import ClassVar
from unittest import mock

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.player.models import Player
from matches import constants
from matches.match.models import Match
from tournaments.round.models import Round
from tournaments.tournament.models import Tournament

from ..models import Participation


class MatchParticipationModelTest(TestCase):
    user: ClassVar[User]
    tournament: ClassVar[Tournament]
    round: ClassVar[Round]

    @classmethod
    def setUpTestData(cls) -> None:
        """
        test対象のモデルに直接関係していないモデルはTestClassで一度だけ初期化する
        """
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
        )
        cls.tournament = Tournament.objects.create()
        cls.round = Round.objects.create(
            tournament=cls.tournament, round_number=1
        )

    def setUp(self) -> None:
        """
        test caseごとに毎回初期化される
        """

        @mock.patch(
            "accounts.player.identicon.generate_identicon",
            return_value="avatars/test.png",
        )
        def _create_player(
            user: User, mock_identicon: mock.MagicMock
        ) -> Player:
            return Player.objects.create(user=user)

        # ParticipationとPlayerとMatchを作成
        self.player = _create_player(self.user)
        self.match = Match.objects.create(round=self.round)

        self.participation = Participation.objects.create(
            match=self.match,
            player=self.player,
            team=constants.ParticipationFields.TeamEnum.ONE.value,
        )

    def test_participation_creation(self) -> None:
        """
        Participationが正常に作成されているかテスト
        """
        # DBの値を反映
        self.player.refresh_from_db()
        self.match.refresh_from_db()
        self.participation.refresh_from_db()

        self.assertEqual(self.participation.player, self.player)
        self.assertEqual(self.participation.match, self.match)

    def test_delete_participation(self) -> None:
        """
        Participationを削除しても、紐づくMatchとPlayerは削除されないことを確認
        """
        player_id = self.player.id
        match_id = self.match.id
        self.participation.delete()

        self.assertFalse(Participation.objects.exists())
        self.assertTrue(Player.objects.filter(id=player_id).exists())
        self.assertTrue(Match.objects.filter(id=match_id).exists())

    def test_delete_player_related_to_participation(self) -> None:
        """
        Playerを削除したら、紐づくParticipationも削除されることを確認
        """
        self.player.delete()

        self.assertFalse(Player.objects.exists())
        self.assertFalse(Participation.objects.exists())

    def test_delete_match_related_to_participation(self) -> None:
        """
        Matchを削除したら、紐づくParticipationも削除されることを確認
        """
        self.match.delete()

        self.assertFalse(Match.objects.exists())
        self.assertFalse(Participation.objects.exists())

    def test_unique_participation_constraint(self) -> None:
        """
        同じ試合に同じプレイヤーが二重に参加できないことを確認
        """
        with self.assertRaises(IntegrityError):
            Participation.objects.create(
                match=self.match,
                player=self.player,
                team=constants.ParticipationFields.TeamEnum.TWO.value,
            )
