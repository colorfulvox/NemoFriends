from django.contrib import admin

from .models import Animal


class AnimalAdmin(admin.ModelAdmin):
    fields = ['species','feeds', 'characteristics', 'commands', 'default_color']

admin.site.register(Animal, AnimalAdmin) 