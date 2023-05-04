from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import PotholeReport

admin.site.register(PotholeReport, OSMGeoAdmin)

# @admin.register(Potholes)
# class PotholeAdmin(OSMGeoAdmin):
#     pass
