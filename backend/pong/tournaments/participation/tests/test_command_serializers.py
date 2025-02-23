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

    def test_max_participation_limit(self) -> None:
        """トーナメントの最大参加者数に達している場合のチェック"""
        # 最大参加者数を超えるデータを作成
        for i in range(constants.MAX_PARTICIPATIONS):
            user = User.objects.create(
                username=f"already_existuser_{i}",
                email=f"already_existtuser_{i}@example.com",
                password="testpassword",
            )
            player = player_models.Player.objects.create(
                user=user, display_name="Test Player"
            )

            participation_models.Participation.objects.create(
                tournament_id=self.tournament.id,
                player_id=player.id,
                participation_name="Player {}".format(i + 1),
            )

        # 参加者がMAX_PARTICIPATIONSを超えた場合、エラーが発生
        data = {
            constants.ParticipationFields.TOURNAMENT_ID: self.tournament.id,
            constants.ParticipationFields.PLAYER_ID: self.player.id,
            constants.ParticipationFields.PARTICIPATION_NAME: "New Player",
        }
        serializer = ParticipationCommandSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_ranking_validation_upper_limit(self):
        """ランキング更新時の範囲チェック"""
        # 参加テーブルを作成
        creation_data = {
            constants.ParticipationFields.TOURNAMENT_ID: self.tournament.id,
            constants.ParticipationFields.PLAYER_ID: self.player.id,
            constants.ParticipationFields.PARTICIPATION_NAME: "New Player",
        }
        create_serializer = ParticipationCommandSerializer(data=creation_data)
        self.assertTrue(create_serializer.is_valid())
        participation = create_serializer.save()

        # ランキングを更新
        update_data = {
            constants.ParticipationFields.RANKING: constants.MAX_PARTICIPATIONS
            + 1
        }  # 不正なランキング

        # エラーになるか
        update_serializer = ParticipationCommandSerializer(
            instance=participation, data=update_data, partial=True
        )
        self.assertFalse(update_serializer.is_valid())
        self.assertIn(
            constants.ParticipationFields.RANKING, update_serializer.errors
        )

    def test_ranking_validation_lower_limit(self) -> None:
        """ランキング更新時の範囲チェック"""
        # 参加テーブルを作成
        creation_data = {
            constants.ParticipationFields.TOURNAMENT_ID: self.tournament.id,
            constants.ParticipationFields.PLAYER_ID: self.player.id,
            constants.ParticipationFields.PARTICIPATION_NAME: "New Player",
        }
        create_serializer = ParticipationCommandSerializer(data=creation_data)
        self.assertTrue(create_serializer.is_valid())
        participation = create_serializer.save()

        # ランキングを更新
        update_data = {
            constants.ParticipationFields.RANKING: 0
        }  # 不正なランキング

        # エラーになるか
        update_serializer = ParticipationCommandSerializer(
            instance=participation, data=update_data, partial=True
        )
        self.assertFalse(update_serializer.is_valid())
        self.assertIn(
            constants.ParticipationFields.RANKING, update_serializer.errors
        )
