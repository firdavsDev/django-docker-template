from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
        )


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={"input_type": "password"})

    def validate(self, attrs):
        self._errors = {}
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            self._errors["errors"] = dict(message=_('Must include "email" and "password'))

        user = authenticate(email=email, password=password)

        if not user:
            self._errors["errors"] = dict(
                message=_("Authenticated has failed, either user is blocked or does not exist")
            )

        if self._errors:
            raise serializers.ValidationError(self._errors)

        attrs["user"] = user
        return attrs
