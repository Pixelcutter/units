from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "owner_id",
            "color_hexcode",
        )

        extra_kwargs = {"id": {"read_only": True}}
