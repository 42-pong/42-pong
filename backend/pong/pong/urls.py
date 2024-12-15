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
    path("api/health/", health_check, name="health-check"),
    # jwt_token
    path("api/token/", include("jwt_token.urls")),
    # accounts
    path("api/accounts/", include("accounts.urls")),
]
