from . import models
from rest_framework import serializers

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = '__all__'

class ArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArrayTest
        fields = '__all__'