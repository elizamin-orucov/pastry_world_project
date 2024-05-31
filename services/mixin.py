from django.db import models


class DateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SlugMixin(DateMixin):
    slug = models.SlugField(unique=True, editable=False)
    code = models.SlugField(unique=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(DateMixin):
    name = models.CharField(max_length=150)

    class Meta:
        abstract = True

