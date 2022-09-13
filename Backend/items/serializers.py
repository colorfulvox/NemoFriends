from .models import Decoration, User_Decoration
from rest_framework import serializers


class ItemsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Decoration
        fields = '__all__'


class ItemsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Decoration
        fields = ('id', 'is_located', 'location', 'angle')