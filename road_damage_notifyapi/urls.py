from django.urls import path
from .views import pothole_details_view

urlpatterns = [
    path('', pothole_details_view),
]