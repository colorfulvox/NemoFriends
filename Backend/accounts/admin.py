from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Mbti

admin.site.register(User, UserAdmin)

class MbtiAdmin(admin.ModelAdmin):
    fieldsets = [
        ('FK',               {'fields': ['animal']}),
        ('mbti', {'fields': ['mbti'],}),
    ]
admin.site.register(Mbti, MbtiAdmin)