from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='timeseries_index'),
    path("line/", views.line_view, name="line"),
    path("timeseries/", views.timeseries_view, name="timeseries"),  # ✅ nouvelle route
    path("stacked_area/", views.stacked_area_view, name="stacked_area"),
    path("candlestick/", views.candlestick_view, name="candlestick"),
    path("multi_line/", views.multi_line_view, name="multi_line"),
    path("bubble/", views.bubble_chart_view, name="bubble"),
    path("radar/", views.radar_chart_view, name="radar"),
    path("treemap/", views.treemap_view, name="treemap"),


]





