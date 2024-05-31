from .filters import BlogFilter
from ..models import Blog, BlogCategory
from rest_framework import generics, filters
from services.pagination import CustomPagination
from django_filters.rest_framework.backends import DjangoFilterBackend
from .serializer import BlogCategorySerializer, BlogListSerializer, BlogDetailSerializer


class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogListSerializer
    pagination_class = CustomPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    filterset_class = BlogFilter
    ordering_fields = ("created_at", "updated_at")


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.filter(published=True)
    serializer_class = BlogDetailSerializer
    lookup_field = "slug"
