from typing import Final

from rest_framework import routers

from . import views

app_name: Final[str] = "friends"

router: routers.DefaultRouter = routers.DefaultRouter()
router.register(r"", views.FriendsViewSet, basename="friends")

urlpatterns = router.urls
