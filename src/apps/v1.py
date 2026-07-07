from django.urls import include, path

urlpatterns = [
    path("account/", include("src.apps.account.urls.account")),
]
