from drf_yasg import openapi
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static


urlpatterns = [
   path("admin/", admin.site.urls),
   path("blog/", include("blogs.api.urls")),
   path("order/", include("order.api.urls")),
   path("basket/", include("basket.api.urls")),
   path("review/", include("reviews.api.urls")),
   path("contact/", include("contact.api.urls")),
   path("product/", include("products.api.urls")),
   path("accounts/", include("accounts.api.urls")),
   path("favorite/", include("favorites.api.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

