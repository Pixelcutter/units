from django.urls import path, re_path
from .views import CategoryListCreateView, CategoryDetailView

app_name = "categories"

urlpatterns = [
    path("", CategoryListCreateView.as_view(), name="category_list_create"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
]
