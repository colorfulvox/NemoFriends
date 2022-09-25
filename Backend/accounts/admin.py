from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Mbti


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_user_animals', 'is_superuser', 'last_login']
    def get_user_animals(self, obj):
        return ', '.join([animal.name for animal in obj.user_animal_set.all()])
    get_user_animals.short_description = 'ANIMALS'
    fieldsets = [
        ('USER INFO',               {'fields':  ['is_superuser','is_staff','is_active','user_permissions', 'first_name', 'last_name', 'email', 'date_joined','password',]}),
        ('GAME INFO', {'fields': ['username', 'gold', 'exp_cnt', 'is_called'],}),
        ('GAME SETTINGS', {'fields': ['bgm', 'effect',],}),
    ]
admin.site.register(get_user_model(), UserAdmin)

class MbtiAdmin(admin.ModelAdmin):
    fieldsets = [
        ('FK',               {'fields': ['animal']}),
        ('MBTI', {'fields': ['mbti'],}),
    ]
admin.site.register(Mbti, MbtiAdmin)