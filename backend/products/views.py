from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from units_api.mixins import UserIsOwnerMixin
import logging

logger = logging.getLogger("debug_to_stdout")


class ProductList(UserIsOwnerMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    # save Product.owner_id as authenticated user.id
    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)

    # confirm authenticated user is owner of product and category (maybe)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # confirm authenticated user is owner of product and category (maybe)
