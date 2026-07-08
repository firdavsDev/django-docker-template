from rest_framework import serializers


class TokenRefreshInputSerializer(serializers.Serializer):
    """Request body for the refresh + logout endpoints (a raw refresh token)."""

    refresh = serializers.CharField()
