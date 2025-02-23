from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.serializers import ValidationError

from accounts.player import models as player_models
from tournaments import constants
from tournaments.tournament import models as tournament_models

from .. import models as participation_models
from ..serializers import ParticipationCommandSerializer


class ParticipationCommandSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # プレーヤーのモックを作成
        self.user = User.objects.create(
            username="testuser_1",
            email="testuser_1@example.com",
            password="testpassword",
        )
        self.player = player_models.Player.objects.create(
            user=self.user, display_name="Test Player"
        )
        self.tournament = tournament_models.Tournament.objects.create()

    def test_successful_creation(self) -> None:
        """正常にデータが作成できる場合"""
        data = {
            constants.ParticipationFields.TOURNAMENT_ID: self.tournament.id,
            constants.ParticipationFields.PLAYER_ID: self.player.id,
            constants.ParticipationFields.PARTICIPATION_NAME: "New Player",
        }
        serializer = ParticipationCommandSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            None,
            serializer.validated_data[constants.ParticipationFields.RANKING],
        )

    def test_missing_tournament_id(self) -> None:
        """必須フィールドであるtournament_idが不足している場合のテスト"""
        data = {
            constants.ParticipationFields.PLAYER_ID: self.player.id,
            constants.ParticipationFields.PARTICIPATION_NAME: "player_x",
        }
        serializer = ParticipationCommandSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            constants.ParticipationFields.TOURNAMENT_ID, serializer.errors
        )

    def test_missing_player_id(self) -> None:
        """必須フィールドであるplayer_idが不足している場合のテスト"""
        data = {
            constants.ParticipationFields.TOURNAMENT_ID: self.tournament.id,
            constants.ParticipationFields.PARTICIPATION_NAME: "player_x",
        }
        serializer = ParticipationCommandSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            constants.ParticipationFields.PLAYER_ID, serializer.errors
        )

    def test_missing_participation_name(self) -> None:
        """必須フィールドであるparticipation_nameが不足している場合のテスト"""
        data = {
            constants.ParticipationFields.TOURNAMENT_ID: self.tournament.id,
            constants.ParticipationFields.PLAYER_ID: self.player.id,
        }
        serializer = ParticipationCommandSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            constants.ParticipationFields.PARTICIPATION_NAME, serializer.errors
        )
