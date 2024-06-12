from django.db import models
from services.mixin import DateMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class Basket(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "Basket"


