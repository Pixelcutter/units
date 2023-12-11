from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
import logging

logger = logging.getLogger("debug_to_stdout")


class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.validated_data["owner_id"] = self.request.user
        return super().perform_create(serializer)


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        owner_id = self.request.user.id
        queryset = Category.objects.filter(owner=owner_id)

        return queryset


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
