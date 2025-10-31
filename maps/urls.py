

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="maps_index"),
    path("scatter/", views.scatter_map_view, name="scatter_map"),
    path("choropleth/", views.choropleth_map_view, name="choropleth_map"),
]
