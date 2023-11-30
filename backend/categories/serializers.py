from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "description",
            "category_owner",
            "color_hexcode",
        )

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=["name", "category_owner"],
                message="You already have a category with this name.",
            )
        ]
