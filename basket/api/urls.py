from . import views
from django.urls import path

app_name = "basket_api"


urlpatterns = [
    path("edit/<int:id>/", views.BasketEditView.as_view(), name="basket_edit"),
    path("", views.BasketListAndCreateView.as_view(), name="basket_list_and_create"),
]
