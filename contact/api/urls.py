from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("about/us/", views.AboutUsView.as_view(), name="about_us"),
    path("us/", views.ContactUsView.as_view(), name="contact_us"),
]
