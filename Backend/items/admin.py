from django.contrib import admin
from .models import Decoration, User_Decoration, Item, User_Item


class DecorationAdmin(admin.ModelAdmin):
    fields = ['cost', 'is_rare']
admin.site.register(Decoration, DecorationAdmin)


class UserDecorationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('FK',               {'fields': ['user','decoration']}),
        ('상세 정보', {'fields': ['is_located', 'location', 'angle'],}),
    ]
admin.site.register(User_Decoration, UserDecorationAdmin)


class ItemAdmin(admin.ModelAdmin):
    readonly_fields  = ['id']
admin.site.register(Item, ItemAdmin) 


class UserItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ('FK',               {'fields': ['user','item']}),
        ('상세 정보', {'fields': ['cnt'],}),
    ]
admin.site.register(User_Item, UserItemAdmin)


