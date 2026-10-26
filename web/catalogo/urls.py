from django.urls import path

from . import views

urlpatterns = [
    path("", views.InicioView.as_view(), name="inicio"),
    path("catalogo/", views.CatalogoView.as_view(), name="catalogo"),
]