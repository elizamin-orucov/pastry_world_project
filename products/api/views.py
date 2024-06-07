from django.db.models import F, IntegerField
from rest_framework import generics
from ..models import Category, Product
from django.db.models.functions import Coalesce
from services.pagination import CustomPagination
from .serializer import CategorySerializer, ProductListSerializer, ProductDetailSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ProductListSerializer

    def get_queryset(self):
        qs = Product.objects.annotate(
            dsc_interest=Coalesce(
                F("discount_interest"), 0, output_field=IntegerField()
            ),
            discount_price=F("price") * F("dsc_interest") / 100,
            total_price=F("price") - F("discount_price")
        ).order_by("-created_at")
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    lookup_field = "slug"
    serializer_class = ProductDetailSerializer

    def get_queryset(self):
        qs = Product.objects.annotate(
            dsc_interest=Coalesce(
                F("discount_interest"), 0, output_field=IntegerField()
            ),
            discount_price=F("price") * F("dsc_interest") / 100,
            total_price=F("price") - F("discount_price")
        ).order_by("-created_at")
        return qs

