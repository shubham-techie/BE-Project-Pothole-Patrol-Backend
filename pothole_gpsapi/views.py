from rest_framework import generics, permissions, views, status
from .models import PotholeReport
from .serializers import PotholeReportSerializer
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter, DistanceToPointOrderingFilter


# class PotholeReportView(generics.ListCreateAPIView):
#     queryset = PotholeReport.objects.all()
#     serializer_class = PotholeReportSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PotholeReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = PotholeReport.objects.all()
        serializer = PotholeReportSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PotholeReportSerializer(data=request.data, context={'request' : request}) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_200_OK)  
    
pothole_report_view = PotholeReportView.as_view()

