from .models import TrafficCamPotholeReport
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from django.contrib.gis.geos import GEOSGeometry
import os
import numpy as np
import statistics as st
from django.conf import settings
# import sys
# sys.path.append("..")
from utility.utils import make_frames_from_video, tf_model, CATEGORIES


class TrafficCamPotholeReportSerializer(GeoModelSerializer):
  class Meta:
    model = TrafficCamPotholeReport
    fields = '__all__'
    read_only_fields = ['id', 'class_label', 'reported_at', 'geo_location']
    
  
  def validate(self, attrs):
    request = self.context.get('request').data
    print(request)

    latitude = request.get('latitude')
    longitude = request.get('longitude')
    video_file = request.get('video_file')

    geo_location = {"type": "Point", "coordinates":[float(longitude), float(latitude)]}
    attrs['geo_location'] = GEOSGeometry(str(geo_location))

    if video_file is None:
      return attrs
    
    upload_path = os.path.join(settings.BASE_DIR, "media", "videos")
    if not os.path.isdir(upload_path):
      os.makedirs(upload_path)

    video_path = os.path.join(upload_path, video_file.name)
    with open(video_path, "wb+") as destination:
      for chunk in video_file.chunks():
        destination.write(chunk)

    video_frames = make_frames_from_video(video_path)
    video_frames = np.array(video_frames)
    video_frames = video_frames.reshape(-1,128,128,3)
    preds = tf_model.predict(video_frames)

    label_idxs = np.argmax(preds, axis=1)
    idx = st.mode(label_idxs)
    class_category = CATEGORIES[idx]
    print(f"Video is of {class_category} road")

    if not idx:
      raise serializers.ValidationError({"class_label" : class_category})
    
    attrs['class_label'] = class_category
    if os.path.isfile(video_path):
      os.remove(video_path)
    
    return attrs
  