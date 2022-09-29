from django.contrib import admin

from .models import Animal, User_Animal


class AnimalAdmin(admin.ModelAdmin):
    list_display = ['id', 'species']
    list_display_links = ['species']
    fields = ['species','feeds', 'features', 'commands',]
admin.site.register(Animal, AnimalAdmin) 


class UserAnimalAdmin(admin.ModelAdmin):
    list_display = ['get_user_animal_id','get_user_animlal', 'user',]
    list_display_links = ['get_user_animlal']
    fieldsets = [
        ('FK',               {'fields': ['user','animal']}),
        ('USER ANIMAL INFO', {'fields': ['name', 'level', 'grade', 'exp'],}),
        ('DETAIL', {'fields': ['is_located', 'talking_cnt', 'playing_cnt', 'last_eating_time']}), 
    ]
    def get_user_animal_id(self, obj):
        return obj.id
    get_user_animal_id.short_description = 'USER_ANIMAL_ID'

    def get_user_animlal(self, obj):
        return f'{obj}({obj.animal})'
    get_user_animlal.short_description = 'ANIMAL(SPECIES)'
    
admin.site.register(User_Animal, UserAnimalAdmin) 