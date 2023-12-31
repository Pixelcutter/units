from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from units_api.mixins import UserIsOwnerMixin
from units_api.permissions import UserIsOwnerPermission
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger("debug_to_stdout")


class CategoryListCreateView(UserIsOwnerMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [UserIsOwnerPermission]


class CategoryDetailView(UserIsOwnerMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [UserIsOwnerPermission]
