from rest_framework import serializers
from .models import UnitsUser
import logging

logger = logging.getLogger("debug_to_stdout")


class UnitsUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UnitsUser
        fields = ["id", "username", "email", "password", "about", "first_name", "last_name"]

    def create(self, validated_data):
        user = UnitsUser.objects.create_user(**validated_data)
        logger.debug(f"created user: {user.id} {user.username} {user.email} {user.password}")
        return user
