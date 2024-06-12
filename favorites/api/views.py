from ..models import Favorite
from rest_framework import generics
from .serializer import FavoriteSerializer
from rest_framework.response import Response
from services.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated


class FavoriteView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = (
        IsAuthenticated,
    )
    pagination_class = CustomPagination

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product")
        favorite, created = Favorite.objects.get_or_create(user=self.request.user, product_id=int(product_id))
        # to delete a product that has been added to the wishlist before
        if not created:
            favorite.delete()
        serializer = self.serializer_class(favorite).data
        return Response(serializer)



