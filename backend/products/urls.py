from django.urls import path, re_path

from .views import ProductList, ProductDetail

app_name = "products"

urlpatterns = [
    path("", ProductList.as_view(), name="product-list-create"),
    path("<int:pk>/", ProductDetail.as_view(), name="product_detail"),
]
