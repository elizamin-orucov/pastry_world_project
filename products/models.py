from django.db import models
from services.slugify import slugify
from services.uploader import Uploader
from ckeditor.fields import RichTextField
from services.generator import CodeGenerator
from mptt.models import MPTTModel, TreeForeignKey
from services.mixin import DateMixin, SlugMixin, BaseModel
from services.choices import DISCOUNT_CHOICES, PRODUCT_STATUS_CHOICES


class Category(MPTTModel, BaseModel):
    name = models.CharField(max_length=70)
    icon = models.ImageField(upload_to=Uploader.category_logo_uploader, blank=True, null=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "Categories"


class Product(BaseModel, SlugMixin):
    description = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    status = models.CharField(max_length=50, choices=PRODUCT_STATUS_CHOICES)
    discount_interest = models.IntegerField(blank=True, null=True, choices=DISCOUNT_CHOICES)

    def __str__(self):
        return self.name

    def create_unique_slug(self, slug, index=0):
        new_slug = slug
        if index:
            new_slug = f"{slug}-{index}"
        qs = self.__class__.objects.filter(slug=new_slug)
        return self.create_unique_slug(slug, index + 1) if qs.exists() else new_slug

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = CodeGenerator.create_product_shortcode(
                size=8, model_=self.__class__
            )
        if not self.slug:
            self.slug = self.create_unique_slug(slugify(title=self.name))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "Products"


class ProductImage(DateMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.product_image_uploader)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "Product images"

