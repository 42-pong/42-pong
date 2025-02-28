import utils.result
from accounts.create_account import create_account
from accounts.user import serializers as user_serializers

from . import serializers

CreateOAuth2UserResult = utils.result.Result[dict, dict]
CreateOAuth2Result = utils.result.Result[dict, dict]


def create_oauth2_user(
    email: str,
    password: str,
    display_name: str,
) -> CreateOAuth2UserResult:
    oauth2_user_data: dict[str, str] = {
        "username": create_account.get_unique_random_username(),
        "email": email,
        "password": password,
    }
    oauth2_user_serializer: user_serializers.UserSerializer = (
        user_serializers.UserSerializer(data=oauth2_user_data)
    )
    if not oauth2_user_serializer.is_valid():
        return CreateOAuth2UserResult.error(oauth2_user_serializer.errors)
    player_data: dict = {"display_name": display_name}
    oauth2_account_result: create_account.CreateAccountResult = (
        create_account.create_account(oauth2_user_serializer, player_data)
    )
    if not oauth2_account_result.is_ok:
        return CreateOAuth2UserResult.error(
            oauth2_account_result.unwrap_error()
        )
    oauth2_user_serializer_data: dict = oauth2_account_result.unwrap()
    return CreateOAuth2UserResult.ok(oauth2_user_serializer_data)


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
    oauth2_serializer.save()
    oauth2_serializer_data: dict = oauth2_serializer.data
    return CreateOAuth2Result.ok(oauth2_serializer_data)
