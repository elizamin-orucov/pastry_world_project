from rest_framework import generics
from ..models import AboutUs, ContactUs
from .serializer import AboutUsSerializer, ContactUsSerializer


class AboutUsView(generics.RetrieveAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutUs.objects.first()


class ContactUsView(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

