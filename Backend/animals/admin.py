from django.contrib import admin

from .models import Animal, User_Animal


class AnimalAdmin(admin.ModelAdmin):
    fields = ['species','feeds', 'features', 'commands',]
admin.site.register(Animal, AnimalAdmin) 


class UserAnimalAdmin(admin.ModelAdmin):
    fieldsets = [
        ('FK',               {'fields': ['user','animal']}),
        ('보유 동물', {'fields': ['name', 'level', 'grade', 'exp'],}),
        ('상세 정보', {'fields': ['color_id','is_located', 'talking_cnt', 'playing_cnt', 'last_eating_time']}), 
    ]
admin.site.register(User_Animal, UserAnimalAdmin) 