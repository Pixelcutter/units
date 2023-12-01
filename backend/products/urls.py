from django.urls import path, re_path

from .views import ProductList, ProductDetail

app_name = "products"

urlpatterns = [
    re_path(r'^$', ProductList.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetail.as_view(), name="product_detail"),
]
