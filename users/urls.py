from django.urls import path
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
    token_verify,
)
from .api import create_user, get_user_profile
from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_confirm,
)

app_name = "users"
urlpatterns = [
    path("token/", token_obtain_pair, name="token_obtain_pair"),
    path("token/refresh/", token_refresh, name="token_refresh"),
    path("token/verify", token_verify, name="token_verify"),
    path("user/profile/", get_user_profile, name="get_user_profile"),
    path("register", create_user, name="create_user"),
    path("reset-password", reset_password_request_token, name="reset_password"),
    path(
        "reset-password/confirm", reset_password_confirm, name="reset_password_confirm"
    ),
]
from .views import GoogleSocialAuthView

urlpatterns += [
    path("auth/google/", GoogleSocialAuthView.as_view(), name="google_login"),
]
