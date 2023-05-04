from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authapi.urls')),
    path('api/pothole-report/', include('pothole_gpsapi.urls')),
    path('api/traffic-pothole-report/', include('video_feedapi.urls')),
    path('api/get-potholes/', include('road_damage_notifyapi.urls')),
] \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
