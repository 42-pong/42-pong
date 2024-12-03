from django.urls import include, path

import jwt_token.urls as jwt_urls

urlpatterns = [
    # jwt token
    path("token/", include(jwt_urls)),
]
