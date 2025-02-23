from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError

from tournaments import constants
from tournaments.participation import models as participation_models
from accounts.player import models as player_models

from .. import models
from ..serializers import TournamentCommandSerializer


class TournamentCommandSerializerTest(TestCase):

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
