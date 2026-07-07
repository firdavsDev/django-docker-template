from django.contrib.auth import get_user_model
from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from ...common.mixins import CustomResponseMixin
from ..serializers.account import AuthTokenSerializer, UserLoginSerializer

User = get_user_model()


class UserObtainTokenAPIView(CustomResponseMixin, ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.AdminRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        user_serializer = UserLoginSerializer(instance=user)
        details = user_serializer.data
        details.update(token=token.key)
        return self.success(message="Login successful", data=details)


user_login_api_view = UserObtainTokenAPIView.as_view()


class LogoutAPIView(CustomResponseMixin, APIView):
    serializer_class = None

    def get(self, request):
        Token.objects.filter(user=request.user).delete()

        return self.success(message="You have successfully logged out")


user_logout_view = LogoutAPIView.as_view()
