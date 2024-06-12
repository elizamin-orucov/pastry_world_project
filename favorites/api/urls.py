from django.urls import path
from . import views

app_name = "favorites_api"

urlpatterns = [
    path("", views.FavoriteView.as_view(), name="favorite"),
]

