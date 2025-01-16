import utils.result
from accounts import create_account

from . import models, serializers

CreateOAuth2UserResult = utils.result.Result[models.User, dict]
CreateOAuth2Result = utils.result.Result[models.OAuth2, dict]


def create_oauth2_user(
    email: str, display_name: str
) -> CreateOAuth2UserResult:
    oauth2_user_data: dict[str, str] = {
        "username": create_account.get_unique_random_username(),
        "email": email,
        "password": "",
    }
    oauth2_user_serializer: serializers.UserSerializer = (
        serializers.UserSerializer(data=oauth2_user_data)
    )
    if not oauth2_user_serializer.is_valid():
        return CreateOAuth2UserResult.error(oauth2_user_serializer.errors)
    player_data: dict = {"display_name": display_name}
    oauth2_account_result = create_account.create_account(
        oauth2_user_serializer, player_data
    )
    if not oauth2_account_result.is_ok:
        return CreateOAuth2UserResult.error(
            oauth2_account_result.unwrap_error()
        )
    oauth2_user: models.User = oauth2_account_result.unwrap()
    return CreateOAuth2UserResult.ok(oauth2_user)


def create_oauth2(
    user_id: int, provider: str, provider_id: str
) -> CreateOAuth2Result:
    oauth2_data = {
        "user": user_id,
        "provider": provider,
        "provider_id": provider_id,
    }
    oauth2_serializer: serializers.OAuth2Serializer = (
        serializers.OAuth2Serializer(data=oauth2_data)
    )
    if not oauth2_serializer.is_valid():
        return CreateOAuth2Result.error(oauth2_serializer.errors)
    oauth2: models.OAuth2 = oauth2_serializer.save()
    return CreateOAuth2Result.ok(oauth2)
