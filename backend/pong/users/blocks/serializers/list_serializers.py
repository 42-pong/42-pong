from rest_framework import serializers as drf_serializers

from accounts import constants as accounts_constants
from users import constants as users_constants
from users import serializers as users_serializers

from .. import constants, models


class BlockRelationshipListSerializer(drf_serializers.ModelSerializer):
    blocked_user = users_serializers.UsersSerializer(
        source="blocked_user.player",
        read_only=True,
        fields=(  # emailは含めない
            accounts_constants.UserFields.ID,
            accounts_constants.UserFields.USERNAME,
            accounts_constants.PlayerFields.DISPLAY_NAME,
            accounts_constants.PlayerFields.AVATAR,
            users_constants.UsersFields.IS_FRIEND,
            users_constants.UsersFields.IS_BLOCKED,
            users_constants.UsersFields.MATCH_WINS,
            users_constants.UsersFields.MATCH_LOSSES,
        ),
    )

    class Meta:
        model = models.BlockRelationship
        fields = (constants.BlockRelationshipFields.BLOCKED_USER,)
