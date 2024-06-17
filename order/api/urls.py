from django.urls import path
from . import views

app_name = "order"


urlpatterns = [
    path("coupon/check/", views.CouponCheckView.as_view(), name="coupon_check"),
    path("create/", views.OrderView.as_view(), name="order_create"),
]
