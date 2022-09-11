from . import models
from rest_framework import serializers

class AnimalsTestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Animal
        fields = '__all__'