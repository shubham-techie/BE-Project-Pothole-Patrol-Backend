from django.db import models
from django.contrib.gis.db.models import PointField

class PotholeDetails(models.Model):
    class Road(models.TextChoices):
        POTHOLED = "POTHOLED", "potholed road"
        UNPAVED = "UNPAVED", "unpaved road"

    geo_location = PointField()
    reported_at = models.DateTimeField(auto_now_add=True)
    class_label = models.CharField(max_length=20, blank=True, choices=Road.choices)
    is_pothole_fixed = models.BooleanField(default=False)
    state = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name_plural = 'PotholeDetails'
        db_table = "potholedetails"

    def __str__(self):
        return self.class_label


class StateRoadAuthority(models.Model):
    state = models.CharField(unique=True, max_length=200)
    email = models.EmailField(unique=True, max_length=254)
    
    class Meta:
        verbose_name_plural = 'StateRoadAuthority'
        db_table = "state_road_authority"

    def __str__(self):
        return self.state
