from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from requests_oauthlib import OAuth2Session
from pong.settings import OAUTH_CLIENT_ID

@api_view(["GET"])
def oauth_authorize(request: Request) -> Response:
    """
    認可エンドポイントを提供する関数
    この関数はクライアント(42pong)が認可サーバーの認可エンドポイントにアクセスし、認可コードを取得するために使用する。
    認可サーバーに接続する際に、redirect_uriを設定する理由は、認可サーバーはクライアントではなくブラウザーにレスポンスを返すため、
    ブラウザからクライアントにリダイレクトし、認可コードを取得する必要があるため。
    """
    client = OAuth2Session(
        client_id=OAUTH_CLIENT_ID, redirect_uri="http://localhost:8000/api/oauth/callback"
    )
    authorization_url, _ = client.authorization_url(
        "https://api.intra.42.fr/oauth/authorize"
    )
    return Response(
        status=302,
        headers={"Location": authorization_url},
    )
