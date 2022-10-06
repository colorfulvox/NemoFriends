from .models import User_Decoration
from rest_framework import serializers


class ItemsPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Decoration
        fields = ('location', 'angle')