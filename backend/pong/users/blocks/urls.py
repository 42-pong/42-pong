from typing import Final

from rest_framework import routers

from . import views

app_name: Final[str] = "blocks"

router: routers.DefaultRouter = routers.DefaultRouter()
router.register(r"", views.BlocksViewSet, basename="blocks")

urlpatterns = router.urls
