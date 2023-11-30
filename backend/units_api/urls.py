from django.urls import path, include

app_name = "units_api"

urlpatterns = [
    path("products/", include("products.urls", namespace="products")),
    path("categories/", include("categories.urls", namespace="categories")),
    # path('auth/', include('authentication.urls', namespace='authentication')),
]
