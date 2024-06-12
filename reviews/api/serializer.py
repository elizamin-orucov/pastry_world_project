from ..models import ProductReview
from rest_framework import serializers
from accounts.api.serializer import UserSerializer


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductReview
        fields = (
            "id",
            "user",
            "rating",
            "content",
            "product",
        )
        extra_kwargs = {
            "product": {"write_only": True}
        }
