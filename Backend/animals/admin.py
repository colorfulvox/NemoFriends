from django.contrib import admin

from .models import Animal, User_Animal


class AnimalAdmin(admin.ModelAdmin):
    fields = ['species','feeds', 'characteristics', 'commands', 'default_color']

admin.site.register(Animal, AnimalAdmin) 


class UserAnimalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user','animal']}),
        ('Animal Information', {'fields': ['name', 'level', 'exp']}),
        ('Detail', {'fields': ['color_id', 'is_located', 'talking_cnt', 'playing_cnt', 'last_eating_time']}), 
    ]

admin.site.register(User_Animal, UserAnimalAdmin) 