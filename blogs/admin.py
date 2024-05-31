from django.contrib import admin
from .models import BlogCategory, BlogImage, Blog


class ImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "code")
    list_filter = ("created_at",)
    search_fields = ("title", "code")
    inlines = ImageInline,


admin.site.register(BlogCategory)
admin.site.register(Blog, BlogAdmin)