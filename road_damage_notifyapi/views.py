from django.shortcuts import render
from rest_framework import generics, views
from .models import PotholeDetails
from .serializers import PotholeDetailSerializer
from rest_framework_gis.filters import DistanceToPointFilter, DistanceToPointOrderingFilter


# class PotholeDetailView(generics.ListAPIView):
#     queryset = PotholeDetails.objects.all()
#     serializer_class = PotholeDetailSerializer

#     distance_filter_field = 'geo_location'
#     distance_filter_convert_meters = True
#     filter_backends = (DistanceToPointFilter,)
#     # distance_ordering_filter_field = 'geo_location'
#     # filter_backends = (DistanceToPointOrderingFilter,)

# pothole_details_view = PotholeDetailView.as_view()

from pothole_gpsapi.models import PotholeReport
from pothole_gpsapi.serializers import PotholeReportSerializer
from rest_framework_gis.filters import DistanceToPointFilter, DistanceToPointOrderingFilter

class PotholeDetailView(generics.ListAPIView):
    queryset = PotholeReport.objects.all()
    serializer_class = PotholeReportSerializer

    distance_filter_field = 'geo_location'
    distance_filter_convert_meters = True
    filter_backends = (DistanceToPointFilter,)
    # distance_ordering_filter_field = 'geo_location'
    # filter_backends = (DistanceToPointOrderingFilter,)

pothole_details_view = PotholeDetailView.as_view()
