from django.test import TestCase
from rest_framework import request as drf_request
from rest_framework import response as drf_response
from rest_framework import status, test

from . import views


class HealthCheckUnitTests(TestCase):
    def test_health_check(self) -> None:
        """
        Unit tes for health_check view.
        GET /health/ returns 200 OK
        """
        factory: test.APIRequestFactory = test.APIRequestFactory()
        request: drf_request.Request = factory.get("/health/")
        response: drf_response.Response = views.health_check(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "OK"})
