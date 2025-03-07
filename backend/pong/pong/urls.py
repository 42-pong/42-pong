"""
URL configuration for pong project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from .health_check.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    # swagger-ui
    path("api/schema/", include("swagger_ui.urls")),
    # health check
    path("api/health/", health_check, name="health_check"),
    # jwt
    path("api/token/", include("jwt.urls")),
    # oauth2
    path("api/oauth2/", include("oauth2.urls")),
    # accounts
    path("api/accounts/", include("accounts.urls")),
    # users
    path("api/users/", include("users.urls")),
    # tournaments
    path("api/tournaments/", include("tournaments.urls")),
    # matches
    path("api/matches/", include("matches.urls")),
	# login
	path("api/login/", include("login.urls")),
]
