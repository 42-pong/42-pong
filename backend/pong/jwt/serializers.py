from rest_framework import serializers


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
