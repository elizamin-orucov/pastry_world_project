from rest_framework import serializers
from django.db.models import F, IntegerField
from django.db.models.functions import Coalesce
from ..models import Product, ProductImage, Category


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = (
            "category_id",
            "category_name"
        )

    def get_category_id(self, obj):
        return obj.id

    def get_category_name(self, obj):
        return obj.name


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    total_price = serializers.FloatField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "image",
            "category",
            "price",
            "total_price",
            "discount_interest",
        )

    def get_image(self, obj):
        image = ProductImageSerializer(obj.productimage_set.first()).data
        return image


class ProductDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField()
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "images",
            "category",
            "price",
            "total_price",
            "discount_interest",
        )

    def get_images(self, obj):
        images_list = obj.productimage_set.all()
        return ProductImageSerializer(images_list, many=True).data

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        other_products_qs = Product.objects.annotate(
            dsc_interest=Coalesce(
                F("discount_interest"), 0, output_field=IntegerField()
            ),
            discount_price=F("price") * F("dsc_interest") / 100,
            total_price=F("price") - F("discount_price")
        ).exclude(id=instance.id).order_by("?")[:8]
        repr_["other_products"] = ProductListSerializer(other_products_qs, many=True).data
        return repr_




