from django.urls import path, re_path
from .views import CategoryList, CategoryDetail

app_name = "categories"

urlpatterns = [
    re_path(r"^$", CategoryList.as_view(), name="category_list"),
    path("<int:pk>/", CategoryDetail.as_view(), name="category_detail"),
]
