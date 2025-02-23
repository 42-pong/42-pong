from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError

from tournaments import constants
from tournaments.participation import models as participation_models
from accounts.player import models as player_models

from .. import models
from ..serializers import TournamentCommandSerializer


class TournamentCommandSerializerTest(TestCase):
    def setUp(self):
        # テスト用のトーナメントインスタンスを作成
        self.tournament = models.Tournament.objects.create(
            status=constants.TournamentFields.StatusEnum.NOT_STARTED.value
        )

    def test_default_status(self):
        """
        `status` が指定されていない場合にデフォルト値が設定されているかを確認するテスト
        """
        serializer_data = {
            constants.TournamentFields.ID: self.tournament.id,
        }
        serializer = TournamentCommandSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())  # バリデーション成功
        self.assertEqual(
            serializer.validated_data[constants.TournamentFields.STATUS],
            constants.TournamentFields.StatusEnum.NOT_STARTED.value,
        )

    def test_on_going_status_with_insufficient_participants(self):
        """
        `status` を `ON_GOING` に変更する際、参加者が足りない場合にエラーが発生するかを確認するテスト
        """
        serializer_data = {
            constants.TournamentFields.STATUS: constants.TournamentFields.StatusEnum.ON_GOING.value,
        }
        serializer = TournamentCommandSerializer(
            self.tournament, data=serializer_data
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_cancelled_status_with_participants(self):
        """
        参加者がいる場合に `status` を `CANCELED` に変更できないことを確認するテスト
        """
        # プレーヤーのモックを作成
        user = User.objects.create(
            username="testuser_1",
            email="testuser_1@example.com",
            password="testpassword",
        )
        player = player_models.Player.objects.create(
            user=user, display_name="Test Player"
        )


        # 参加者を追加
        participation_models.Participation.objects.create(
            tournament=self.tournament,
            player=player,
            participation_name="Player 1",
        )

        serializer_data = {
            constants.TournamentFields.STATUS: constants.TournamentFields.StatusEnum.CANCELED.value,
        }
        serializer = TournamentCommandSerializer(
            self.tournament, data=serializer_data
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
