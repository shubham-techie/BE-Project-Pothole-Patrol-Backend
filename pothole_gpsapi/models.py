from django.db import models
from django.contrib.auth.models import User
from road_damage_notifyapi.models import PotholeDetails

class PotholeReport(PotholeDetails):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    road_img = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        verbose_name_plural = 'PotholeReport'
        db_table = "user_pothole_report"

    def __str__(self):
        return self.road_img.name