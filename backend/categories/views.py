from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from units_api.mixins import UserIsOwnerMixin
from units_api.permissions import IsOwnerPermission
import logging

logger = logging.getLogger("debug_to_stdout")


class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.validated_data["owner_id"] = self.request.user
        return super().perform_create(serializer)


class CategoryList(UserIsOwnerMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerPermission]
