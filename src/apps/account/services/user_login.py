from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from ...account.models import User


def login(email: str, password: str) -> dict:
    """Authenticate by email/password and return token payload.

    Raises AuthenticationFailed on bad credentials; the view layer wraps
    the result via CustomResponseMixin.
    """
    user = User.objects.filter(email=email).first()
    if user is None or not user.check_password(password):
        raise AuthenticationFailed("login failed, incorrect login or password")

    token, _ = Token.objects.get_or_create(user=user)
    return {"id": user.id, "token": token.key}
