from dataclasses import fields
from . import models
from rest_framework import serializers
class UserChangeBGMSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('bgm',)

class UserChangeEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('effect',)
        