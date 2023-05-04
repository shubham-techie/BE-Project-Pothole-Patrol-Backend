from rest_framework import generics
from .models import TrafficCamPotholeReport
from .serializers import TrafficCamPotholeReportSerializer


class TrafficCamPotholeReportView(generics.ListCreateAPIView):
    queryset = TrafficCamPotholeReport.objects.all()
    serializer_class = TrafficCamPotholeReportSerializer

traffic_cam_pothole_report_view = TrafficCamPotholeReportView.as_view()
