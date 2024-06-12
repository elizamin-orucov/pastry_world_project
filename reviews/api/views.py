from ..models import ProductReview
from rest_framework import generics
from .serializer import ProductReviewSerializer
from services.pagination import CustomPagination
from services.permissions import ReviewsPermission
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class ProductReviewsView(generics.ListCreateAPIView):
    lookup_field = "product_id"
    pagination_class = CustomPagination
    serializer_class = ProductReviewSerializer
    permission_classes = IsAuthenticatedOrReadOnly,

    def get_queryset(self):
        product_id = self.kwargs.get(self.lookup_field)
        return ProductReview.objects.filter(product_id=int(product_id))

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ProductReviewEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = (
        IsAuthenticated,
        ReviewsPermission
    )
    lookup_field = "id"

    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)


