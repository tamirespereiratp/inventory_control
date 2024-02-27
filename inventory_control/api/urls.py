from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.category import CategoryList, CategoryDetail

app_name = "api"
urlpatterns = [
    path("categories/", CategoryList.as_view(), name="categories-list"),
    path("categories/<int:pk>", CategoryDetail.as_view(), name="categories-list"),
]
urlpatterns = format_suffix_patterns(urlpatterns)