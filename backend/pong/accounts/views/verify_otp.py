import logging
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import permissions, request, response, status, views
from rest_framework import serializers as drf_serializers

from pong.custom_response import custom_response
from utils import result

from .. import constants
from ..create_account import create_account
from ..two_factor_authentication.otp import constants as otp_constants
from ..two_factor_authentication.otp import serializers as otp_serializers
from ..two_factor_authentication.otp import (
    user_serializers as user_serializers,
)
from ..two_factor_authentication.temporary_user import models as two_fa_models

CreateAccountResult = result.Result[dict, dict]

logger = logging.getLogger(__name__)


class VerifyOTPView(views.APIView):
    """
    OTPを検証し、アカウントを作成するビュー
    """

    serializer_class: type[user_serializers.UserSerializer] = (
        user_serializers.UserSerializer
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

    def post(self, request: request.Request) -> response.Response:
        """
        OTPを検証し、アカウントを作成するPOSTメソッド
        """

        def _create_account(temp_user: two_fa_models.TemporaryUser) -> dict:
            hashed_password: str = temp_user.password
            user_data: dict[str, str] = {
                constants.UserFields.EMAIL: temp_user.email,
                constants.UserFields.PASSWORD: hashed_password,
            }
            create_account_result: CreateAccountResult = (
                create_account.create_account(
                    user_serializer=user_serializers.UserSerializer(
                        data=user_data
                    ),
                    player_data={},
                )
            )
            if create_account_result.is_error:
                logger.error(
                    f"Failed to create account: {create_account_result.unwrap_error()}"
                )
                raise ValidationError(create_account_result.unwrap_error())
            return create_account_result.unwrap()

        def _verify_otp_and_create_user(email: str, otp: str) -> dict:
            try:
                # TemporaryUserを取得
                temp_user: two_fa_models.TemporaryUser = (
                    two_fa_models.TemporaryUser.objects.get(email=email)
                )
            except two_fa_models.TemporaryUser.DoesNotExist:
                logger.error(f"TemporaryUser not found: {email}")
                raise ValidationError("TemporaryUser not found")

            # OTPを検証
            opt_data: dict = {
                otp_constants.OptFields.TEMP_USER: temp_user.id,
                otp_constants.OptFields.OTP_CODE: otp,
            }
            otp_serializer: otp_serializers.OTPSerializer = (
                otp_serializers.OTPSerializer(data=opt_data)
            )
            otp_serializer.is_valid(raise_exception=True)

            # アカウントを作成
            account_data: dict = _create_account(temp_user)
            # TemporaryUserは不要なので削除
            temp_user.delete()
            return account_data

        email: Optional[str] = request.data.get(constants.UserFields.EMAIL)
        otp: Optional[str] = request.data.get(otp_constants.OptFields.OTP_CODE)

        # todo: 時間があれば修正したい仮のassert。email,otpどちらかがNoneの場合は400を返したい
        assert email is not None, "Email is required"
        assert otp is not None, "OTP is required"
        try:
            with transaction.atomic():
                # OTPを検証し、成功したらユーザーを作成する
                validated_data: dict = _verify_otp_and_create_user(email, otp)
            # todo: logger.info追加
            return custom_response.CustomResponse(
                data=validated_data, status=status.HTTP_201_CREATED
            )
        except drf_serializers.ValidationError as e:
            logger.error(f"[400] ValidationError: {str(e)}")
            # e.detail: list or dictのためmypy用にlistの処理も書いているが、ほぼdictだと思われる
            if isinstance(e.detail, list):
                errors: dict = {"ValidationError": e.detail}
            else:
                errors = e.detail
            return custom_response.CustomResponse(
                code=[otp_constants.Code.INVALID],
                errors=errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            logger.error(f"[400] ValidationError: {str(e)}")
            return custom_response.CustomResponse(
                code=[otp_constants.Code.INVALID],
                errors={"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            # DatabaseErrorなど
            logger.error(f"[500] Failed to verify otp): {str(e)}")
            raise
