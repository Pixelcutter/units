from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer


class CategoryList(generics.ListCreateAPIView):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        owner_id = self.request.GET.get("owner_id", None)
        queryset = Category.objects.filter(category_owner=owner_id)
        # params = "query params:" + self.request.GET.get("name", "-- nope --")
        # logger.debug(params)
        return queryset


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
