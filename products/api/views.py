from .filters import ProductFilter
from ..models import Category, Product
from rest_framework import generics, filters
from django.db.models.functions import Coalesce
from services.pagination import CustomPagination
from django.db.models import F, IntegerField, Avg
from django_filters.rest_framework.backends import DjangoFilterBackend
from .serializer import CategorySerializer, ProductListSerializer, ProductDetailSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    pagination_class = CustomPagination
    serializer_class = ProductListSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ("created_at", "updated_at")

    def get_queryset(self):
        qs = Product.objects.annotate(
            dsc_interest=Coalesce(
                F("discount_interest"), 0, output_field=IntegerField()
            ),
            discount_price=F("price") * F("dsc_interest") / 100,
            total_price=F("price") - F("discount_price"),
            rating=Avg(F("productreview__rating"))
        ).order_by("-created_at", "-rating")
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

