from rest_framework import serializers
from .models import UnitsUser
import logging

logger = logging.getLogger("debug_to_stdout")


class UnitsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitsUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UnitsUser.objects.create_user(**validated_data)
        return user
