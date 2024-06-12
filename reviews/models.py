from django.db import models
from services.choices import RATING
from services.mixin import DateMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductReview(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "Product reviews"



