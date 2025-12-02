from django.urls import path
from . import views

app_name = "banks"

urlpatterns = [
    path("map/", views.bank_map, name="map"),
]
