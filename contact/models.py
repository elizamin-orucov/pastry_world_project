from django.db import models
from services.mixin import DateMixin, BaseModel


class AboutUs(DateMixin):
    history = models.TextField()

    def __str__(self):
        return "About Us"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        addition_qs = AboutUsAddition.objects.all()
        # it prevents the AboutUsAddition model from updating when it is empty.
        addition_qs.update(about_us_id=self.id) if addition_qs.exists() else None
        self.__class__.objects.exclude(id=self.id).delete()

    class Meta:
        verbose_name = "history"
        verbose_name_plural = "About Us"


class AboutUsAddition(BaseModel):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "addition"
        verbose_name_plural = "About Us Addition"


