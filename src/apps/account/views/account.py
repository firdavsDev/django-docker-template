from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ...common.mixins import CustomResponseMixin
from ..serializers.account import (
    AuthTokenSerializer,
    RegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from ..services.user_login import login


class UserLoginAPIView(CustomResponseMixin, APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login(request=request, **serializer.validated_data)

        data = UserLoginSerializer(instance=result["user"]).data
        data["token"] = result["token"]
        return self.success(message="Login successful", data=data)


user_login_api_view = UserLoginAPIView.as_view()


class RegisterAPIView(CustomResponseMixin, APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return self.success(
            message="Registration successful",
            data=UserSerializer(instance=user).data,
            status_code=201,
        )


register_api_view = RegisterAPIView.as_view()


class MeAPIView(CustomResponseMixin, APIView):
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        return self.success(message="OK", data=self.serializer_class(instance=request.user).data)


me_api_view = MeAPIView.as_view()


class LogoutAPIView(CustomResponseMixin, APIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return self.success(message="You have successfully logged out")


user_logout_view = LogoutAPIView.as_view()
