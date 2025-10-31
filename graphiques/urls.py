from django.urls import path
from . import views

urlpatterns = [
    path("histogram/", views.histogram_view, name="histogram"),
    path("scatter/", views.scatter_view, name="scatter"),  # ✅ nouvelle route
    path("boxplot/", views.boxplot_view, name="boxplot"),  # ✅ nouvelle route
    path("bar/", views.bar_view, name="bar"),
    path("pie/", views.pie_view, name="pie"),  # ✅ nouveau
    path("line/", views.line_view, name="line"),
    path("heatmap/", views.heatmap_view, name="heatmap"),

]




