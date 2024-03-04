from rest_framework import generics
from .serializer import (
    LoginSerializer, RegisterSerializer, ActivationCheckSerializer, ResetPasswordSerializer,
    ResetPasswordCheckSerializer, ResetPasswordCompleteSerializer
)
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str

User = get_user_model()


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationCheckView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationCheckSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=int(id_))


class ResetPasswordView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer


class ResetPasswordCheckView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordCheckSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=int(id_))


class ResetPasswordCompleteView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordCompleteSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get("uuid")
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=int(id_))


