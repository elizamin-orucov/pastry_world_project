from django.contrib.auth import get_user_model
from django.urls import path
from . import views

User = get_user_model()

app_name = "accounts_api"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("reset/password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path("activation/<uuid>/", views.ActivationCheckView.as_view(), name="activation"),
    path("reset/password/check/<uuid>/", views.ResetPasswordCheckView.as_view(), name="reset_password_check"),
    path("reset/password/complete/<uuid>/", views.ResetPasswordCompleteView.as_view(), name="reset_password_complete"),
]
