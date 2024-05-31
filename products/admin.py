from django.contrib import admin
from .models import Category, Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "code")
    list_display_links = ("name", "status")
    search_fields = ("name", "code")
    list_filter = ("status",)
    inlines = ImageInline,


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)


