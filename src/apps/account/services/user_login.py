from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


def login(email: str, password: str, request=None) -> dict:
    """Authenticate by email/password and return the user + auth token.

    Raises AuthenticationFailed on bad credentials or a disabled account.
    The view layer wraps the result via CustomResponseMixin.
    """
    user = authenticate(request=request, email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Authentication failed: user does not exist or password is incorrect.")
    if not user.is_active:
        raise AuthenticationFailed("This account is disabled.")

    token, _ = Token.objects.get_or_create(user=user)
    return {"user": user, "token": token.key}
