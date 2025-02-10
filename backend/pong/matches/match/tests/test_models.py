from unittest.mock import MagicMock, patch

from django.test import TestCase

from tournaments.round.models import Round
from tournaments.tournament.models import Tournament

from ..models import Match


class MatchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        test対象のモデルに直接関係していないモデルはTestClassで一度だけ初期化する
        """
        cls.tournament = Tournament.objects.create()

    def setUp(self) -> None:
        """
        test caseごとに毎回初期化される
        """
        self.round = Round.objects.create(
            tournament=self.tournament, round_number=1
        )
        self.match = Match.objects.create(round=self.round)
