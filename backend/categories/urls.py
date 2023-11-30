from django.urls import path
from .views import CategoryList, CategoryDetail

app_name = "categories"

urlpatterns = [
    path("", CategoryList.as_view(), name="category_list"),
    path("<int:pk>/", CategoryDetail.as_view(), name="category_detail"),
]
