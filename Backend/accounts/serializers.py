from dataclasses import fields

from items.models import User_Item, Decoration
from . import models
from rest_framework import serializers
from animals.models import User_Animal, Animal
class UserChangeBGMSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('bgm',)

class UserChangeEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('effect',)
        
class UserAnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Animal
        fields = ('id', 'name', 'animal_id', 'grade', 'level', 'exp', 'color_id',
                  'last_eating_time', 'playing_cnt', 'talking_cnt',
                  'created_at','is_located')
class UserItemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Item
        fields = ('item_id','cnt')
        
class AnimalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ('id','species','feeds','features','commands')
        
class ShopInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Decoration
        fields = ('id', 'cost')