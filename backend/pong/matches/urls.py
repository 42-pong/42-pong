from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# DefaultRouter を使用 (自動で一覧・詳細のルートを作成)
router = DefaultRouter()
router.register(r"", views.MatchReadOnlyViewSet, basename="")

urlpatterns = [
    path("", include(router.urls)),  # router のルートを include
]
