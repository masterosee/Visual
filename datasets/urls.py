from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='datasets_index'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
