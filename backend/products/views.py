from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from units_api.mixins import UserIsOwnerMixin
from units_api.permissions import UserIsOwnerPermission
from rest_framework.parsers import MultiPartParser, FormParser
import logging

logger = logging.getLogger("debug_to_stdout")


class ProductList(UserIsOwnerMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [UserIsOwnerPermission]
    parser_classes = [MultiPartParser, FormParser]

    # save Product.owner_id as authenticated user.id
    # def perform_create(self, serializer):
    #     serializer.save(owner_id=self.request.user)


class ProductDetail(UserIsOwnerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [UserIsOwnerPermission]
