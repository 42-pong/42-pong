from django.test import TestCase

from oauth2 import serializers


class UserSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.Serializer = serializers.UserSerializer

    def test_true(self) -> None:
        self.assertTrue(True)


class OAuth2SerializerTestCase(TestCase):
    def setUp(self) -> None:
        # self.user = User.objects.create_user()
        self.Serializer = serializers.OAuth2Serializer

    def test_true(self) -> None:
        self.assertTrue(True)


class FortyTwoTokenSerializerTestCase(TestCase):
    def setUp(self) -> None:
        # self.oauth2 = OAuth2.objects.create()
        self.Serializer = serializers.FortyTwoTokenSerializer

    def test_true(self) -> None:
        self.assertTrue(True)
