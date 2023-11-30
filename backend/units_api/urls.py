from django.urls import path, include

app_name = 'units_api'

patterns = [
    path('products/', include('products.urls', namespace='products')),
]