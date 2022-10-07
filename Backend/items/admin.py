from django.contrib import admin
from .models import Decoration, User_Decoration


class DecorationAdmin(admin.ModelAdmin):
    list_display = ['id', 'cost', 'is_rare']
    fields = ['cost', 'is_rare']
admin.site.register(Decoration, DecorationAdmin)


class UserDecorationAdmin(admin.ModelAdmin):
    list_display = ['get_user_decoration_id', 'user', 'decoration', 'is_located']
    fieldsets = [
        ('FK',               {'fields': ['user','decoration']}),
        ('DETAIL', {'fields': ['is_located', 'location', 'angle'],}),
    ]
    def get_user_decoration_id(self, obj):
        return obj.id
    get_user_decoration_id.short_description = 'USER_DECORATION_ID'
admin.site.register(User_Decoration, UserDecorationAdmin)

