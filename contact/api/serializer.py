from rest_framework import serializers
from ..models import AboutUs, AboutUsAddition, ContactUs


class AboutUsAdditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUsAddition
        fields = (
            "name",
            "description"
        )


class AboutUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = (
            "history",
        )

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        addition_qs = instance.aboutusaddition_set.all()
        repr_["addition"] = AboutUsAdditionSerializer(addition_qs, many=True).data
        return repr_


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = (
            "full_name",
            "subject",
            "message"
        )
