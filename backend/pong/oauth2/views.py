# views.py
from urllib.parse import urlencode

import requests
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from pong.settings import (
    OAUTH2_AUTHORIZATION_ENDPOINT,
    OAUTH2_CLIENT_ID,
    OAUTH2_CLIENT_SECRET_KEY,
    OAUTH2_TOKEN_ENDPOINT,
    PONG_ORIGIN,
)


@api_view(["GET"])
def oauth2_authorize(request: Request) -> Response:
    """
    認可エンドポイントを呼ぶ関数
    この関数はクライアント(42pong)が認可サーバーの認可エンドポイントにアクセスし、認可コードを取得するために使用する。
    認可サーバーに接続する際に、redirect_uriを設定する理由は、認可サーバーはクライアントではなくブラウザーにレスポンスを返すため、
    ブラウザからクライアントにリダイレクトし、認可コードを取得する必要があるため。

    認可エンドポイントを呼ぶケース
    - ユーザーが新規アカウントを作成した時
    - ユーザーが明示的にログアウトした時(ログアウト時にアクセストークンを削除する場合)
    - リフレッシュトークンの有効期限が切れた時
    """

    query_params = {
        "client_id": OAUTH2_CLIENT_ID,
        "redirect_uri": PONG_ORIGIN + reverse("oauth2_callback"),
        "response_type": "code",
        # todo: csrf対策の為にstate追加するかも
    }
    query_string = urlencode(query_params)

    authorization_url = f"{OAUTH2_AUTHORIZATION_ENDPOINT}?{query_string}"

    return Response(
        status=302,
        headers={"Location": authorization_url},
    )


@api_view(["GET"])
def oauth2_callback(request: Request) -> Response:
    """
    認可サーバーからのレスポンスを受け取る関数
    この関数は認可サーバーからのレスポンスを受け取り、認可コードを取得するために使用する。
    """
    # todo: Result型で定義する？
    code = request.GET.get("code")
    if not code:
        return Response(
            {
                "error": "Authorization code is None. Please check your authentication process."
            },
            status=400,
        )
    request_data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": PONG_ORIGIN + reverse("oauth2_callback"),
        "client_id": OAUTH2_CLIENT_ID,
        "client_secret": OAUTH2_CLIENT_SECRET_KEY,
    }
    response = requests.post(
        OAUTH2_TOKEN_ENDPOINT,
        data=request_data,
    )
    tokens = response.json()
    # todo アプリケーションのホームURLを設定する(仮)
    # app_home_url = ""
    # return Response({"message": "Home page"}, status=200, headers={"Host": app_home_url})
    return Response(
        {
            f"Callback: {PONG_ORIGIN + reverse("oauth2_callback")}, Token: {tokens}"
        },
        status=200,
    )
