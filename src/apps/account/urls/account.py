from django.urls import path

from ..views import account

app_name = "account"

urlpatterns = [
    path(
        "register/",
        view=account.register_api_view,
        name="register",
    ),
    path(
        "login/",
        view=account.user_login_api_view,
        name="login_view",
    ),
    path(
        "logout/",
        view=account.user_logout_view,
        name="user_logout",
    ),
    path(
        "me/",
        view=account.me_api_view,
        name="me",
    ),
]
