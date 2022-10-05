from dataclasses import fields

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from items.models import User_Item, Decoration
from . import models
from rest_framework import serializers
from animals.models import User_Animal, Animal
from django.conf import settings
import jwt

class UserChangeSoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('bgm','effect')

class UserAnimalInfoSerializer(serializers.ModelSerializer):
    last_eating_time = serializers.DateTimeField(format='%Y%m%d%H%M%S')
    created_at = serializers.DateField(format='%Y/%m/%d')
    class Meta:
        model = User_Animal
        fields = ('id', 'name', 'animal_id', 'grade', 'level', 'exp', 
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
        
        
class MyTokenRefreshSerializer(TokenRefreshSerializer):
        # response 커스텀 
    default_error_messages = {
        'no_active_account': {'message':'username or password is incorrect!',
                              'success': False,
                              'status' : 401}
    }
    # 유효성 검사
    def validate(self, attrs):
        data = super().validate(attrs)

        data['access_token'] = data['access']

        return data

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
