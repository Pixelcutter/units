from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    # queryset = Product.productobjects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.productobjects.all()
        print("query params", end=" ")
        for q in self.request.query_params:
            print(q, end=" ")
        return queryset


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.productobjects.all()
    serializer_class = ProductSerializer
