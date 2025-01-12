import utils.result
from accounts import create_account

from . import models, serializers

CreateOAuth2UserResult = utils.result.Result[models.User, dict]
CreateOAuth2Result = utils.result.Result[models.OAuth2, dict]
CreateFortyTwoTokenResult = utils.result.Result[models.FortyTwoToken, dict]
CreateFortyTwoAuthorizationResult = utils.result.Result[models.OAuth2, dict]


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
    oauth2_user_serializer.is_valid(raise_exception=True)
    player_data: dict = {"display_name": display_name}
    oauth2_account_result = create_account.create_account(
        oauth2_user_serializer, player_data
    )
    if not oauth2_account_result.is_ok:
        CreateOAuth2UserResult.error(oauth2_account_result.unwrap_error())
    oauth2_user: models.User = oauth2_account_result.unwrap()
    return CreateOAuth2UserResult.ok(oauth2_user)


def _create_oauth2(user_id: int, provider_id: str) -> CreateOAuth2Result:
    oauth2_data = {
        "user": user_id,
        "provider": "42",
        "provider_id": provider_id,
    }
    oauth2_serializer: serializers.OAuth2Serializer = (
        serializers.OAuth2Serializer(data=oauth2_data)
    )
    if not oauth2_serializer.is_valid():
        return CreateOAuth2Result.error(oauth2_serializer.errors)
    try:
        oauth2: models.OAuth2 = oauth2_serializer.save()
        return CreateOAuth2Result.ok(oauth2)
    except Exception as e:
        return CreateOAuth2Result.error({"Error": e})


def _create_forty_two_token(tokens: dict) -> CreateFortyTwoTokenResult:
    forty_two_token_serializer: serializers.FortyTwoTokenSerializer = (
        serializers.FortyTwoTokenSerializer(data=tokens)
    )
    if not forty_two_token_serializer.is_valid():
        return CreateFortyTwoTokenResult.error(
            forty_two_token_serializer.errors
        )
    try:
        forty_two_token: models.FortyTwoToken = (
            forty_two_token_serializer.save()
        )
        return CreateFortyTwoTokenResult.ok(forty_two_token)
    except Exception as e:
        return CreateFortyTwoTokenResult.error({"Error": e})


# todo: 汎用的な関数にできるかも
def create_forty_two_authorization(
    user_id: int, provider_id: str, tokens: dict
) -> CreateFortyTwoAuthorizationResult:
    # todo: oauth2の作成とforty_two_tokenの作成をトランザクションで処理する
    oauth2_result: CreateOAuth2Result = _create_oauth2(user_id, provider_id)
    if not oauth2_result.is_ok:
        return CreateFortyTwoAuthorizationResult.error(
            oauth2_result.unwrap_error()
        )
    oauth2: models.OAuth2 = oauth2_result.unwrap()
    tokens["oauth2"] = oauth2.id
    forty_two_token_result: CreateFortyTwoTokenResult = (
        _create_forty_two_token(tokens)
    )
    if not forty_two_token_result.is_ok:
        oauth2.delete()
        return CreateFortyTwoAuthorizationResult.error(
            forty_two_token_result.unwrap_error()
        )
    return CreateFortyTwoAuthorizationResult.ok(oauth2)
