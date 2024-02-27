from django.urls import path
from . import views
from .views import SuppliersListView, SuppliersSearchView, SuppliersCreateView, SuppliersDeleteView, SuppliersUpdateView

app_name = 'suppliers'

urlpatterns = [
    path("", SuppliersListView.as_view(), name = "index"),
    path("cadastro/", SuppliersCreateView.as_view(), name="create"),
    path("<int:pk>/delete", SuppliersDeleteView.as_view(), name="delete"),
    path("search", SuppliersSearchView.as_view(), name="search"),
    path("<slug:slug>/", SuppliersUpdateView.as_view(), name="update"),
    path("<int:id>/toggle_enabled", views.toggle_enabled, name="toggle_enabled"),
]
