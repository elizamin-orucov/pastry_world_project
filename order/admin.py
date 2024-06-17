from django.contrib import admin
from django.contrib import admin
from .models import Coupon, Order, OrderItem


class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "valid_from", "valid_to", "active")
    list_filter = ("active", "valid_from", "valid_to")
    search_fields = ("code",)


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon, CouponAdmin)
