from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "category",
            "owner_id",
            "quantity",
            "for_sale",
            "price",
            "image",
        )

        extra_kwargs = {"id": {"read_only": True}}
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Product.objects.all(),
                fields=["name", "owner_id"],
                message="Product name must be unique for each user",
            )
        ]
