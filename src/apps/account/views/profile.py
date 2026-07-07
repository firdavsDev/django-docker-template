from rest_framework.views import APIView

from ...common.mixins import CustomResponseMixin
from ..serializers import UserLoginSerializer


class MeAPIView(CustomResponseMixin, APIView):
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        return self.success(message="OK", data=self.serializer_class(instance=request.user).data)


me_api_view = MeAPIView.as_view()
