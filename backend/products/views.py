from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.productobjects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.productobjects.all()
    serializer_class = ProductSerializer
