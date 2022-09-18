from dataclasses import fields
from . import models
from rest_framework import serializers


class AnimalsRenameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User_Animal
        fields = ('name',)


class AnimalColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User_Animal
        fields = ('color',)


class AnimalsTestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Animal
        fields = '__all__'