import django_filters
from django_filters import filterset
from ..models import Product, Category
from services.choices import PRODUCT_STATUS_CHOICES


class ProductFilter(filterset.FilterSet):
    status = django_filters.ChoiceFilter(field_name="status", choices=PRODUCT_STATUS_CHOICES)
    rating = django_filters.NumberFilter(field_name="rating", label="rating", lookup_expr="gte")
    total_price = django_filters.RangeFilter(field_name="total_price", label="total price range")
    search = django_filters.CharFilter(field_name="name", label="search", lookup_expr="icontains")
    category = django_filters.ModelChoiceFilter(field_name="category", queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = (
            "rating",
            "status",
            "search",
            "category",
            "total_price"
        )


