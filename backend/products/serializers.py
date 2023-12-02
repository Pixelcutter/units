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
            "image_url",
        )
