from rest_framework import generics
from ..models import Coupon, Order
from .serializer import CouponSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.pagination import CustomPagination


class CouponCheckView(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = IsAuthenticated,

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = IsAuthenticated,
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.method == "GET":
            return Order.objects.filter(user=self.request.user).order_by("-created_at")
        return Order.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



