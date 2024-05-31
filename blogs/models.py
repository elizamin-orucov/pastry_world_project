from django.db import models
from ckeditor.fields import RichTextField
from services.generator import CodeGenerator
from django.contrib.auth import get_user_model
from services.mixin import SlugMixin, DateMixin, BaseModel
from services.uploader import Uploader
from services.slugify import slugify

User = get_user_model()


class BlogCategory(BaseModel):

    def __str__(self):
        return self.name


class Blog(SlugMixin):
    title = models.CharField(max_length=150)
    content = RichTextField()
    categories = models.ManyToManyField(BlogCategory, related_name="category")
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
            self.slug = self.create_unique_slug(slugify(title=self.title))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "blog"
        verbose_name_plural = "Blogs"


class BlogImage(DateMixin):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.blog_image_uploader)

    def __str__(self):
        return self.blog.title

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "Blog images"







