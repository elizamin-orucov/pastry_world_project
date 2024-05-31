from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [
    path("list/", views.BlogListView.as_view(), name="blog_list"),
    path("detail/<slug>/", views.BlogDetailView.as_view(), name="blog_detail"),
    path("category/list/", views.BlogCategoryListView.as_view(), name="blog_category_list"),
]
