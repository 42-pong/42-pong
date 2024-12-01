from django.urls import include, path

import jwt.urls as jwt_urls

urlpatterns = [
    # jwt token
    path("token/", include(jwt_urls)),
]
