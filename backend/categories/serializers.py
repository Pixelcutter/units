from rest_framework.exceptions import ValidationError
from .models import Category
from django.db import IntegrityError
from rest_framework import serializers


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
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=["name", "owner_id"],
                message="Category name must be unique for each user",
            )
        ]