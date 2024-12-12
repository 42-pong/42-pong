from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from requests_oauthlib import OAuth2Session
from pong.settings import OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET_KEY
import requests

@api_view(["GET"])
def oauth_authorize(request: Request) -> Response:
    """
    認可エンドポイントを提供する関数
    この関数はクライアント(42pong)が認可サーバーの認可エンドポイントにアクセスし、認可コードを取得するために使用する。
    認可サーバーに接続する際に、redirect_uriを設定する理由は、認可サーバーはクライアントではなくブラウザーにレスポンスを返すため、
    ブラウザからクライアントにリダイレクトし、認可コードを取得する必要があるため。
    """

    query_params = {
        "client_id": OAUTH_CLIENT_ID,
        "redirect_uri": "http://localhost:8000/api/oauth/callback",
        "response_type": "code",
        # todo: csrf対策の為にstate追加するかも
    }
    query_string = urlencode(query_params)

    authorization_url = (
        f"https://api.intra.42.fr/oauth/authorize?{query_string}"
    )

    return Response(
        status=302,
        headers={"Location": authorization_url},
    )


@api_view(["GET"])
def oauth_callback(request: Request) -> Response:
    """
    認可サーバーからのレスポンスを受け取る関数
    この関数は認可サーバーからのレスポンスを受け取り、認可コードを取得するために使用する。
    """
    # todo: Result型で定義する？
    code = request.GET.get("code")
    if not code:
        return Response({"error": "Authorization code is None. Please check your authentication process."}, status=400)
    request_data = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/api/oauth/callback",
        "client_id": OAUTH_CLIENT_ID,
        "client_secret": OAUTH_CLIENT_SECRET_KEY,
    }
    response = requests.post(
        "https://api.intra.42.fr/oauth/token",
        data=request_data,
    )
    #todo トークンを取得した後、ユーザーを作成し、データベースに保存する？
    tokens = response.json()
    # todo アプリケーションのホームURLを設定する
    # app_home_url = "https://github.com/42-pong"
    # return Response({"message": "Redirecting to home page"}, status=302, headers={"Location": app_home_url})
    return Response({f"Token: {tokens}"}, status=200)

@api_view(["POST"])
def oauth_fetch_token(request: Request) -> Response:
    """
    トークンエンドポイントを提供する関数
    この関数は認可サーバーから認可コードを使用してトークンを取得するために使用する。
    """
    try:
        response = requests.post(
            "https://api.intra.42.fr/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=request.data,
        )
        return (response.json(), response.status_code)
    except Exception as e:
        return Response(
            {"error": f"Failed to fetch token: {str(e)}"}, status=400
        )
