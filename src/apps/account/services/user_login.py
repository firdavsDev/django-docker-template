from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


def tokens_for_user(user) -> dict:
    """Mint a fresh JWT access/refresh pair for the given user."""
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def login(email: str, password: str, request=None) -> dict:
    """Authenticate by email/password and return the user + JWT token pair.

    Raises AuthenticationFailed on bad credentials or a disabled account.
    The view layer wraps the result via CustomResponseMixin.
    """
    user = authenticate(request=request, email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Authentication failed: user does not exist or password is incorrect.")
    if not user.is_active:
        raise AuthenticationFailed("This account is disabled.")

    return {"user": user, **tokens_for_user(user)}
