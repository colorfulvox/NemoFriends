from .models import Decoration, User_Decoration
from rest_framework import serializers


class ItemsCreateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Decoration
        fields = '__all__'


class ItemsUpdateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Decoration
        fields = ('id', 'is_located', 'location', 'angle')