from django.contrib import admin
from .models import AboutUs, AboutUsAddition, ContactUs


class AdditionInline(admin.TabularInline):
    model = AboutUsAddition
    extra = 0


class AboutUsAdmin(admin.ModelAdmin):
    inlines = AdditionInline,


admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(ContactUs)

