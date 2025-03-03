class TokenExpiredError(Exception):
    """トークンの有効期限切れを示す例外"""

    def __init__(
        self, message: str = "Token has expired", code: str = "token_expired"
    ):
        super().__init__(message)
        self.code = code


class InvalidTokenError(Exception):
    """不正なトークンを示す例外"""

    def __init__(
        self,
        message: str = "Token is an invalid token",
        code: str = "invalid_token",
    ):
        super().__init__(message)
        self.code = code
