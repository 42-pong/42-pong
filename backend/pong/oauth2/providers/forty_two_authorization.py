import utils.result

from .. import create_oauth2_account, models, serializers

CreateFortyTwoTokenResult = utils.result.Result[models.FortyTwoToken, dict]
CreateFortyTwoAuthorizationResult = utils.result.Result[models.OAuth2, dict]


def _create_forty_two_token(tokens: dict) -> CreateFortyTwoTokenResult:
    forty_two_token_serializer: serializers.FortyTwoTokenSerializer = (
        serializers.FortyTwoTokenSerializer(data=tokens)
    )
    if not forty_two_token_serializer.is_valid():
        return CreateFortyTwoTokenResult.error(
            forty_two_token_serializer.errors
        )
    forty_two_token: models.FortyTwoToken = forty_two_token_serializer.save()
    return CreateFortyTwoTokenResult.ok(forty_two_token)


def create_forty_two_authorization(
    user_id: int, provider: str, provider_id: str, tokens: dict
) -> CreateFortyTwoAuthorizationResult:
    # todo: oauth2の作成とforty_two_tokenの作成をトランザクションで処理する
    oauth2_result: create_oauth2_account.CreateOAuth2Result = (
        create_oauth2_account.create_oauth2(user_id, provider, provider_id)
    )
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
