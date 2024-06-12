from django.urls import path
from . import views

app_name = "reviews_api"

urlpatterns = [
    path("edit/<int:id>/", views.ProductReviewEditView.as_view(), name="product_review_edit"),
    path("list/<int:product_id>/", views.ProductReviewsView.as_view(), name="product_review_list"),
]

