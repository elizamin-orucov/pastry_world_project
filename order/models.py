from django.db import models
from django.utils import timezone
from services.mixin import DateMixin
from services.generator import CodeGenerator
from django.contrib.auth import get_user_model
from services.choices import ORDER_STATUS_CHOICES

User = get_user_model()


class Coupon(DateMixin):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to


class Order(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subtotal = models.FloatField(default=0)
    total = models.FloatField(default=0)
    code = models.SlugField(unique=True)
    shipping_address = models.CharField(max_length=250, blank=True, null=True)
    shipping_address_name = models.CharField(max_length=250, blank=True, null=True, default="Free")
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="Order Received")

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator().create_product_shortcode(size=12, model_=self.__class__)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "Orders"


class OrderItem(DateMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=50)
    total_price = models.FloatField()

    def __str__(self):
        return self.order.user.email

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "Items"

