from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)
from .managers import CustomUserManager
from services.generator import CodeGenerator


def upload_to(instance, filename):
    return f"users/{instance.email}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=120)
    username = models.CharField(unique=True, max_length=250)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    slug = models.SlugField(unique=True)
    activation_code = models.CharField(max_length=6, blank=True, null=True, editable=False)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "user"
        verbose_name_plural = "User Accounts"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = CodeGenerator.create_slug_shortcode(size=20, model_=self.__class__)
        if not self.logo:
            # default image for users without a profile picture
            default_logo_path = "static/user/user-logo.png"
            self.logo.save("default_user_logo.jpg", open(default_logo_path, "rb"), save=False)
        return super(User, self).save(*args, **kwargs)

