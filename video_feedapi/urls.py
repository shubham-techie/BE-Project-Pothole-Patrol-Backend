from django.urls import path
from .views import traffic_cam_pothole_report_view

urlpatterns = [
    path('', traffic_cam_pothole_report_view),
]