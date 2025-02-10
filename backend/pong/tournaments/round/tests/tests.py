from django.test import TestCase

from tournaments.constants import RoundFields
from tournaments.tournament.models import Tournament

from ..models import Round


class RoundModelTest(TestCase):
    def setUp(self) -> None:
        # テスト用のトーナメントデータを作成
        self.tournament = Tournament.objects.create()
        # Player作成
        self.round: Round = Round.objects.create(
            tournament=self.tournament,
            round_number=1,
        )

    def test_create_round(self) -> None:
        """
        ラウンドが正常に作成されるかテスト
        """
        # 作成したラウンドがデータベースに正しく保存されていることを確認
        self.assertEqual(self.round.tournament, self.tournament)
        self.assertEqual(self.round.round_number, 1)
        self.assertEqual(
            self.round.status, RoundFields.StatusEnum.IN_PROGRESS.value
        )

    def test_change_round_status(self) -> None:
        """
        ラウンドのステータスを更新できることを確認
        """
        # ラウンドを更新
        self.round.status = RoundFields.StatusEnum.COMPLETED.value
        self.round.save()

        # DB の最新状態を取得
        self.round.refresh_from_db()

        self.assertEqual(
            self.round.status, RoundFields.StatusEnum.COMPLETED.value
        )

    def test_delete_round(self) -> None:
        """
        Roundを削除したら、紐づくTournamentは削除されないことを確認
        """
        tournament_id = self.tournament.id
        self.round.delete()

        self.assertFalse(Round.objects.exists())
        self.assertTrue(Tournament.objects.filter(id=tournament_id).exists())

    def test_delete_related_tournament(self) -> None:
        """
        Tournamentを削除したら、紐づくRoundも削除されることを確認
        """
        self.tournament.delete()

        self.assertFalse(Round.objects.exists())
        self.assertFalse(Tournament.objects.exists())
