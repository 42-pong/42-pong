from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):  # type: ignore
    """
    OpenAPI 用のカスタム JWT 認証スキーム拡張クラス
    """

    target_class = "jwt.authentication.CustomJWTAuthentication"
    name = "jwtAuth"

    def get_security_definition(self, auto_schema: AutoSchema) -> dict:
        """
        OpenApiAuthenticationExtensionが提供するOpenAPI の認証方式を定義する関数

        本メソッドをオーバーライドし、JWT の Bearer 認証方式を使用するように設定する
        """
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix="Bearer",
            bearer_format="JWT",
        )  # type: ignore
