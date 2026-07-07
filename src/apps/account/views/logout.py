from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from ...common.mixins import CustomResponseMixin
from ..serializers import TokenRefreshInputSerializer


class LogoutAPIView(CustomResponseMixin, APIView):
    serializer_class = TokenRefreshInputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError as exc:
            raise InvalidToken(str(exc)) from exc

        # The stateless access token stays valid until it expires.
        return self.success(message="You have successfully logged out")


user_logout_view = LogoutAPIView.as_view()
