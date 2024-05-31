from rest_framework import serializers
from ..models import BlogCategory, BlogImage, Blog


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = (
            "image",
        )


class BlogCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogCategory
        fields = (
            "category_id",
            "category_name",
        )

    def get_category_id(self, obj):
        return obj.id

    def get_category_name(self, obj):
        return obj.name


class BlogListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    categories = BlogCategorySerializer(read_only=True, many=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = (
            "title",
            "slug",
            "image",
            "created_at",
            "categories",
        )

    def get_image(self, obj):
        return BlogImageSerializer(obj.blogimage_set.first()).data

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %B %Y")


class BlogDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    categories = BlogCategorySerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = (
            "title",
            "content",
            "images",
            "author",
            "created_at",
            "categories",
        )

    def get_images(self, obj):
        return BlogImageSerializer(obj.blogimage_set.all(), many=True).data

    def get_author(self, obj):
        return obj.author.full_name

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %B %Y")

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        other_blogs = Blog.objects.exclude(id=instance.id)
        repr_["other blogs"] = BlogListSerializer(other_blogs, many=True).data
        return repr_
