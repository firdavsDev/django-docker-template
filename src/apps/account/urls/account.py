from django.urls import path

from .. import views

app_name = "account"

urlpatterns = [
    path(
        "register/",
        view=views.register_api_view,
        name="register",
    ),
    path(
        "login/",
        view=views.user_login_api_view,
        name="login_view",
    ),
    path(
        "token/refresh/",
        view=views.token_refresh_api_view,
        name="token_refresh",
    ),
    path(
        "logout/",
        view=views.user_logout_view,
        name="user_logout",
    ),
    path(
        "me/",
        view=views.me_api_view,
        name="me",
    ),
]
