from django.urls import path
from .views import pothole_report_view

urlpatterns=[
    path('', pothole_report_view),
] 
