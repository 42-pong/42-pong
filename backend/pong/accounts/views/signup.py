import logging
import random
import string
from typing import Optional

from django.db import transaction
from drf_spectacular import utils
from rest_framework import permissions, request, response, status, views

from pong.custom_response import custom_response

from .. import constants
from ..player import serializers as player_serializers
from ..two_factor_authentication.otp import constants as otp_constants
from ..two_factor_authentication.otp import models as otp_models
from ..two_factor_authentication.temporary_user import (
    serializers as temp_user_serializers,
)

logger = logging.getLogger(__name__)


# todo: class名変更したい
class AccountCreateView(views.APIView):
    """
    新規アカウントを作成するサインアップ時に呼ばれるビュー
    実際のアカウント作成はしない
    """

    serializer_class: type[player_serializers.PlayerSerializer] = (
        player_serializers.PlayerSerializer
    )
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)

    def handle_exception(self, exc: Exception) -> response.Response:
        """
        APIViewのhandle_exception()をオーバーライド
        viewでtry-exceptしていない例外をカスタムレスポンスに変換して返す
        """
        # AllowAnyなので認証エラーは発生しない

        logger.error(f"[500] Internal server error: {str(exc)}")
        response: custom_response.CustomResponse = (
            custom_response.CustomResponse(
                code=[constants.Code.INTERNAL_ERROR],
                errors={"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )
        return response

    @utils.extend_schema(
        request=utils.OpenApiRequest(
            player_serializers.PlayerSerializer,
            examples=[
                utils.OpenApiExample(
                    "Example request",
                    value={
                        constants.UserFields.EMAIL: "user@example.com",
                        constants.UserFields.PASSWORD: "test12345",
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
                                constants.UserFields.EMAIL: "user@example.com",
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
            500: utils.OpenApiResponse(
                description="Internal server error",
                response={
                    "type": "object",
                    "properties": {
                        custom_response.STATUS: {"type": "string"},
                        custom_response.CODE: {"type": "list"},
                    },
                },
                examples=[
                    utils.OpenApiExample(
                        "Example 500 response",
                        value={
                            custom_response.STATUS: custom_response.Status.ERROR,
                            custom_response.CODE: [
                                constants.Code.INTERNAL_ERROR
                            ],
                        },
                    ),
                ],
            ),
        },
    )
    def post(
        self, request: request.Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        """
        サインアップ時に呼ばれるPOSTメソッド
        emailとpasswordを受け取り、emailに対してワンタイムパスワードを送信する
        email,password,otpを仮のテーブルに保存しておく
        """

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

        email: Optional[str] = request.data.get(constants.UserFields.EMAIL)

        try:
            with transaction.atomic():
                # TemporaryUserにemail,hash化したpasswordを一時的に保存
                temp_user_serializer: temp_user_serializers.TemporaryUserSerializer = temp_user_serializers.TemporaryUserSerializer(
                    data=request.data
                )
                if not temp_user_serializer.is_valid():
                    return _handle_validation_error(
                        temp_user_serializer.errors
                    )
                temp_user = temp_user_serializer.save()

                # OPTを生成してDBに保存
                otp: str = generate_otp()
                otp_models.OTP.objects.create(
                    temp_user=temp_user, otp_code=otp
                )

                # todo: 時間があれば修正したい仮のassert。email,otpどちらかがNoneの場合は400を返したい
                assert email is not None, "Email is required"
                # OTPの保存に成功したらメールを送信
                send_otp_to_email(email, otp)

            # todo: できれば`/verify/otp/`のリダイレクトLocationを追加したい
            return custom_response.CustomResponse(
                data={constants.UserFields.EMAIL: email},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # DatabaseErrorなど
            logger.error(f"[500] Failed to create account: {str(e)}")
            raise


# todo: ファイル移動したい
def generate_otp() -> str:
    """
    6桁のOTPを生成する
    """
    otp: str = "".join(
        random.choices(string.digits, k=otp_constants.OPT_CODE_LENGTH)
    )
    return otp


# todo: ファイル移動したい
# todo: email宛てにOTPを送信する
def send_otp_to_email(email: str, otp: str) -> None:
    """
    OTPをメールで送信する
    """
    pass
