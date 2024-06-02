from rest_framework import generics
from ..models import AboutUs
from .serializer import AboutUsSerializer


class AboutUsView(generics.RetrieveAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutUs.objects.first()

