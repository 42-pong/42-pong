from django.urls import path
from drf_spectacular import views

urlpatterns = [
    # 'api/schema/'
    path("", views.SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        views.SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
