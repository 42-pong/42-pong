import logging

from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views

from pong.custom_response import custom_response
from users import constants as users_constants

from . import constants
from .create_account import create_account
from .player import serializers as player_serializers
from .user import serializers as user_serializers

logger = logging.getLogger(__name__)


class AccountCreateView(views.APIView):
    """
    新規アカウントを作成するビュー
    """

    serializer_class: type[player_serializers.PlayerSerializer] = (
        player_serializers.PlayerSerializer
    )
    permission_classes = (permissions.AllowAny,)

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            player_serializers.PlayerSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        constants.UserFields.EMAIL: "user@example.com",
                        constants.UserFields.PASSWORD: "passwordpassword",
                    },
                ),
            ],
        ),
        responses={
            201: utils.OpenApiResponse(
                response=player_serializers.PlayerSerializer,
                examples=[
                    utils.OpenApiExample(
                        "Example 201 response",
                        value={
                            custom_response.STATUS: custom_response.Status.OK,
                            custom_response.DATA: {
                                constants.UserFields.ID: 2,
                                constants.UserFields.USERNAME: "username",
                                constants.UserFields.EMAIL: "user@example.com",
                                constants.PlayerFields.DISPLAY_NAME: "default",
                                constants.PlayerFields.AVATAR: "/media/avatars/sample.png",
                                users_constants.UsersFields.IS_FRIEND: False,
                                users_constants.UsersFields.IS_BLOCKED: False,
                                users_constants.UsersFields.MATCH_WINS: 0,
                                users_constants.UsersFields.MATCH_LOSSES: 0,
                            },
                        },
                    ),
                ],
            ),
            400: utils.OpenApiResponse(
                description="Invalid Request (複数例あり)",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": ["string"]},
                        custom_response.CODE: {"type": ["list"]},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 400 response - already_exists",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.ALREADY_EXISTS
                            ],
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 400 response - invalid_email",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.INVALID_EMAIL
                            ],
                        },
                    ),
                    utils.OpenApiExample(
                        "Example 400 response - invalid_password",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.INVALID_PASSWORD
                            ],
                        },
                    ),
                ],
            ),
            # todo: 詳細のschemaが必要であれば追加する
            500: utils.OpenApiResponse(description="Internal server error"),
        },
    )
    def post(
        self, request: request.Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        """
        新規アカウントを作成するPOSTメソッド
        requestをSerializerに渡してvalidationを行い、
        有効な場合はPlayerとUserを作成してDBに追加し、作成されたアカウント情報をresponseとして返す
        """

        def _create_user_serializer(
            user_data: dict,
        ) -> user_serializers.UserSerializer:
            # usernameのみBEがランダムな文字列をセット
            user_data[constants.UserFields.USERNAME] = (
                create_account.get_unique_random_username()
            )
            # user_dataの中に必須fieldが存在しない場合は、UserSerializerでエラーになる
            return user_serializers.UserSerializer(data=user_data)

        def _handle_validation_error(errors: dict) -> response.Response:
            code: list[str] = []
            # emailのエラーがあればcodeに追加
            if constants.UserFields.EMAIL in errors:
                # codeの取得に失敗した場合は呼び出し元のexceptに入る
                email_code: str = errors[constants.UserFields.EMAIL][0].code
                if email_code == "unique":
                    code.append(constants.Code.ALREADY_EXISTS)
                    logger.error(
                        "[400] Failed to create account: email already exists"
                    )
                else:
                    # 既にアカウント登録済み以外は全てINVALID_EMAIL
                    code.append(constants.Code.INVALID_EMAIL)
                    logger.error(
                        "[400] Failed to create account: invalid email format"
                    )
            # passwordのエラーがあればcodeに追加
            if constants.UserFields.PASSWORD in errors:
                code.append(constants.Code.INVALID_PASSWORD)
                logger.error(
                    "[400] Failed to create account: invalid password format"
                )
            return custom_response.CustomResponse(
                code=code,
                errors=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        def _handle_unexpected_error(errors: dict) -> response.Response:
            # 実装上のミスor予期せぬエラーのみ
            logger.error("[500] Failed to create account")
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors=errors,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            # サインアップ専用のUserSerializerを作成
            user_serializer: user_serializers.UserSerializer = (
                _create_user_serializer(request.data)
            )
            if not user_serializer.is_valid():
                return _handle_validation_error(user_serializer.errors)

            # 作成したUserSerializerを使って新規アカウントを作成
            create_account_result: create_account.CreateAccountResult = (
                create_account.create_account(
                    user_serializer,
                    request.data,
                )
            )
            if create_account_result.is_error:
                return _handle_unexpected_error(
                    create_account_result.unwrap_error()
                )

            user_serializer_data: dict = create_account_result.unwrap()
            # todo: logger.info()追加
            return custom_response.CustomResponse(
                data=user_serializer_data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"[500] Failed to create account: {str(e)}")
            return custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
