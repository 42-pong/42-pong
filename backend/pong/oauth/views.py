from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from requests_oauthlib import OAuth2Session
from pong.settings import OAUTH_CLIENT_ID

@api_view(["GET"])
def oauth_authorize(request: Request) -> Response:
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
