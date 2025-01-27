from django.urls import include, path
from rest_framework import routers

from .tournament import views as tournament_views

router = routers.DefaultRouter()
router.register(r"", tournament_views.TournamentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
