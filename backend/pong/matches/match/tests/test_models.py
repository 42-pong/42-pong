from typing import ClassVar

from django.test import TestCase

from tournaments.round.models import Round
from tournaments.tournament.models import Tournament

from ..models import Match


class MatchModelTest(TestCase):
    tournament: ClassVar[Tournament]

    @classmethod
    def setUpTestData(cls) -> None:
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

    def test_match_creation(self) -> None:
        """
        Matchが正常に作成されるかテスト
        """
        # DBの値を反映
        self.round.refresh_from_db()
        self.match.refresh_from_db()

        self.assertEqual(self.match.round, self.round)

    def test_delete_match(self) -> None:
        """
        Matchを削除し、紐づくRoundは削除されないことを確認
        """
        round_id = self.round.id
        self.match.delete()

        self.assertFalse(Match.objects.exists())
        self.assertTrue(Round.objects.filter(id=round_id).exists())

    def test_delete_round_deletes_match(self) -> None:
        """
        Roundを削除し、紐づくMatchも削除されることを確認
        """
        self.round.delete()

        self.assertFalse(Round.objects.exists())
        self.assertFalse(Match.objects.exists())
