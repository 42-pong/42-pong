from django.urls import include, path
from rest_framework import routers

from .participation import views as participation_views
from .tournament import views as tournament_views

router = routers.DefaultRouter()
# この順番でregisterしないとparticipationsのエンドポイントのURIマッチングが通らない
router.register(
    r"participations",
    participation_views.ParticipationReadOnlyViewSet,
    basename="participation",
)
router.register(
    r"", tournament_views.TournamentReadOnlyViewSet, basename="tournament"
)

urlpatterns = [
    path("", include(router.urls)),
]
