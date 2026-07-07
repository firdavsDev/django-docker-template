from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ...common.mixins import CustomResponseMixin
from ..serializers import RegisterSerializer, UserSerializer
from ..services.user_login import tokens_for_user


class RegisterAPIView(CustomResponseMixin, APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = UserSerializer(instance=user).data
        data.update(tokens_for_user(user))
        return self.success(message="Registration successful", data=data, status_code=201)


register_api_view = RegisterAPIView.as_view()
