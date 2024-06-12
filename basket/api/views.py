from ..models import Basket
from rest_framework import generics
from .serializer import BasketSerializer
from rest_framework.response import Response
from services.pagination import CustomPagination
from services.permissions import BasketPermission
from rest_framework.permissions import IsAuthenticated


class BasketListAndCreateView(generics.ListCreateAPIView):
    serializer_class = BasketSerializer
    permission_classes = IsAuthenticated,
    pagination_class = CustomPagination

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        quantity = request.data.get("quantity", 1)

        basket, created = Basket.objects.get_or_create(
            user=self.request.user, product_id=int(product_id),
            defaults={"quantity": int(quantity)}
        )
        if not created:
            basket.quantity = int(quantity)
            basket.save()

        serializer = self.serializer_class(basket).data
        return Response(serializer)


class BasketEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, BasketPermission)
    serializer_class = BasketSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

