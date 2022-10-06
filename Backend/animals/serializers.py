from dataclasses import field, fields
from . import models
from rest_framework import serializers


class UserAnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User_Animal
        fields = '__all__'
        depth = 1
        

class AnimalColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User_Animal
        fields = ('color',)


class AnimalsTestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Animal
        fields = '__all__'


