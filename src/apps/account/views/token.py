from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from ...common.mixins import CustomResponseMixin


class TokenRefreshAPIView(CustomResponseMixin, APIView):
    """Exchange a refresh token for a new access token.

    Delegates rotation + blacklisting to simplejwt's TokenRefreshSerializer, which
    honours ROTATE_REFRESH_TOKENS / BLACKLIST_AFTER_ROTATION; result is enveloped.
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(str(exc)) from exc

        return self.success(message="Token refreshed", data=serializer.validated_data)


token_refresh_api_view = TokenRefreshAPIView.as_view()
