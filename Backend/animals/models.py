from django.db import models

class Animal(models.Model):
    species = models.TextField()
    feeds = models.JSONField(default=list)
    characteristics = models.JSONField(default=list)
    commands = models.JSONField(default=list)
    default_color = models.IntegerField()
