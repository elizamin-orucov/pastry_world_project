from rest_framework import serializers
from ..models import Product, ProductImage, Category


# class CategorySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Category
#         fields = (
#             "id",
#             "name"
#         )
#
#
# class ProductImageSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = ProductImage
#         fields = ("image",)
#
#
# class ProductListSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     total_price = serializers.FloatField()
#     image = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = (
#             "name",
#             "image",
#             "category",
#             "price",
#             "total_price",
#             "discount_interest",
#         )
#
#     def get_image(self, obj):
#         image = ProductImageSerializer(obj.productimage_set.first()).data
#         return image

