from rest_framework import serializers
from ..models import Coupon, Order, OrderItem
from products.models import Product
from basket.models import Basket
from django.db.models import F, FloatField
from django.db.models.functions import Coalesce
from products.api.serializer import ProductImageSerializer


class CouponSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)

    class Meta:
        model = Coupon
        fields = (
            "code",
            "discount"
        )
        extra_kwargs = {
            "discount": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context.get("user")

        try:
            code = Coupon.objects.get(code=attrs.get("code"))
        except:
            raise serializers.ValidationError({"error": "no coupon found"})

        if not code.is_valid():
            raise serializers.ValidationError({"error": "coupon is no longer active"})
        if user in code.users.all():
            raise serializers.ValidationError({"error": "you used this coupon"})

        return super().validate(attrs)

    def create(self, validated_data):
        code = validated_data.get("code")
        return Coupon.objects.get(code=code)


class OrderItemListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "image",
            "quantity",
            "total_price",
        )

    def get_image(self, obj):
        qs = Product.objects.filter(code=obj.sku)
        product = qs.get() if qs else None
        image = product.productimage_set.first() if product else None
        return ProductImageSerializer(image).data


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "subtotal",
            "total",
            "shipping_address_name",
            "shipping_address",
        )

    def create(self, validated_data):
        user = self.context.get("user")

        basket_list = Basket.objects.annotate(
            discount_interest=Coalesce(F("product__discount_interest"), 0, output_field=FloatField()),
            product_disc_prc=F("product__price") * F("discount_interest") / 100,
            total_price=F("product__price") - F("product_disc_prc"),
            subtotal=F("total_price") * F("quantity")
        ).filter(user=user)

        new_order = Order.objects.create(
            **validated_data, user=user
        )

        for _ in basket_list:
            OrderItem.objects.create(
                order=new_order,
                product_id=_.product.id,
                sku=_.product.code,
                quantity=_.quantity,
                total_price=_.total_price
            )
        return new_order

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        items = instance.order_items.all()
        repr_["order items"] = OrderItemListSerializer(items, many=True).data
        repr_["delivery location"] = {
            "address title": instance.shipping_address_name,
            "location": instance.shipping_address
        }
        return repr_


