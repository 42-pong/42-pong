from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.serializers import ValidationError

from accounts.player import models as player_models
from tournaments import constants
from tournaments.participation import models as participation_models

from .. import models
from ..serializers import TournamentCommandSerializer


class TournamentCommandSerializerTest(TestCase):
    def setUp(self) -> None:
        # テスト用のトーナメントインスタンスを作成
        self.tournament = models.Tournament.objects.create(
            status=constants.TournamentFields.StatusEnum.NOT_STARTED.value
        )

    @mock.patch(
        "accounts.player.identicon.generate_identicon",
        return_value="avatars/test.png",
    )
    def _create_player(
        self, user: User, display_name: str, mock_identicon: mock.MagicMock
    ) -> player_models.Player:
        return player_models.Player.objects.create(
            user=user, display_name=display_name
        )

    def test_default_status(self) -> None:
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

    def test_on_going_status_with_insufficient_participants(self) -> None:
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

    def test_cancelled_status_with_participants(self) -> None:
        """
        参加者がいる場合に `status` を `CANCELED` に変更できないことを確認するテスト
        """
        # プレーヤーのモックを作成
        user = User.objects.create(
            username="testuser_1",
            email="testuser_1@example.com",
            password="testpassword",
        )
        player = self._create_player(user, "Test Player")

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

    def test_cancelled_status_without_participants(self) -> None:
        """
        参加者がいない場合に `status` を `CANCELED` に変更できることを確認するテスト
        """
        serializer_data = {
            constants.TournamentFields.STATUS: constants.TournamentFields.StatusEnum.CANCELED.value,
        }
        serializer = TournamentCommandSerializer(
            self.tournament, data=serializer_data
        )
        self.assertTrue(serializer.is_valid())  # バリデーション成功
        self.assertEqual(
            serializer.validated_data[constants.TournamentFields.STATUS],
            constants.TournamentFields.StatusEnum.CANCELED.value,
        )
