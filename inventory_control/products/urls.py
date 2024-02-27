from django.urls import path
from . import views
from .views import CategoryListView

app_name = 'products'
urlpatterns = [
    path("", views.index, name = "index"),
    path("cadastro/", views.create, name="create"),
    path("<int:id>/delete", views.delete, name="delete"),
    path("search", views.search, name="search"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
    path("categorias/", CategoryListView.as_view(), name="categories"),
    path("categories/search", views.search_categories, name="categories_search"),
    path("categorias/cadastro/", views.create_category, name="category_create"),
    path("categorias/<slug:slug>/", views.update_category, name="category_update"),
    path("categories/<int:id>/delete", views.delete_category, name="category_delete"),
    path("<slug:slug>/", views.update, name="update"),
    path('suppliers/<int:id>/', views.get_suppliers_from_product, name='suppliers')
]