from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from ...common.mixins import CustomResponseMixin
from ..serializers import AuthTokenSerializer, UserLoginSerializer
from ..services.user_login import login


class UserLoginAPIView(CustomResponseMixin, APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "auth"
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login(request=request, **serializer.validated_data)

        data = UserLoginSerializer(instance=result["user"]).data
        data["access"] = result["access"]
        data["refresh"] = result["refresh"]
        return self.success(message="Login successful", data=data)


user_login_api_view = UserLoginAPIView.as_view()
