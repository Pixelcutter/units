from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
import logging

logger = logging.getLogger("debug_to_stdout")


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # queryset = Product.objects.filter(product_owner=self.request.user.id)
        queryset = Product.objects.all()

        for_sale_filter = self.request.query_params.get("for_sale", None)
        if for_sale_filter is not None:
            queryset = queryset.filter(for_sale=for_sale_filter)

        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.productobjects.all()
    serializer_class = ProductSerializer
