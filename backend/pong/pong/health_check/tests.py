from django.test import TestCase
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

from .views import health_check


class HealthCheckUnitTests(TestCase):
    def test_health_check(self) -> None:
        """
        Unit tes for health_check view.
        GET /health/ returns 200 OK
        """
        factory: APIRequestFactory = APIRequestFactory()
        request: Request = factory.get("/health/")
        response: Response = health_check(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"status": "OK"})
