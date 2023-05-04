from rest_framework import serializers
from .models import PotholeDetails

class PotholeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotholeDetails
        fields = '__all__'