from django.urls import path, re_path
from .views import CategoryList, CreateCategoryView, CategoryDetail

app_name = "categories"

urlpatterns = [
    path("create/", CreateCategoryView.as_view(), name="create_category"),
    path("", CategoryList.as_view(), name="category_list"),
    path("<int:pk>/", CategoryDetail.as_view(), name="category_detail"),
]
