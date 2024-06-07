from django.urls import path
from . import views

app_name = "products_api"

urlpatterns = [
    path("list/", views.ProductListView.as_view(), name="list"),
    path("detail/<slug>/", views.ProductDetailView.as_view(), name="detail"),
]
