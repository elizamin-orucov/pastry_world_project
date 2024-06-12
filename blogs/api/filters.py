import django_filters
from ..models import Blog, BlogCategory


class BlogFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="title", label="search", lookup_expr="icontains")
    categories = django_filters.ModelMultipleChoiceFilter(
        field_name="categories", label="categories", queryset=BlogCategory.objects.all()
    )

    class Meta:
        model = Blog
        fields = (
            "search",
            "categories",
        )
