from rest_framework import serializers

from Service.models import VehicleType


class VehicleTypeSerializer(serializers.Serializer):

    class Meta:
        model = VehicleType




