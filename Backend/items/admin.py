from django.contrib import admin
from .models import Decoration, User_Decoration, Color, User_Color


class DecorationAdmin(admin.ModelAdmin):
    fields = ['cost', 'is_rare']

admin.site.register(Decoration, DecorationAdmin)


class UserDecorationAdmin(admin.ModelAdmin):
    fields = ['user', 'decoration', 'is_located', 'location', 'angle']

admin.site.register(User_Decoration, UserDecorationAdmin)


class ColorAdmin(admin.ModelAdmin):
    readonly_fields  = ['id']

admin.site.register(Color, ColorAdmin) 


class UserColorAdmin(admin.ModelAdmin):
    fields = ['user', 'color', 'cnt']

admin.site.register(User_Color, UserColorAdmin)


