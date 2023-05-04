from django.db import models
from road_damage_notifyapi.models import PotholeDetails

class TrafficCamPotholeReport(PotholeDetails):
    camera_no = models.IntegerField()
    area_name = models.CharField(max_length=100)
    video_file = models.FileField(upload_to="videos/", blank=True)

    class Meta:
        verbose_name_plural = 'TrafficCamPotholeReport'
        db_table = "trafficcam_pothole_report"

    def __str__(self):
        return self.video_file.name