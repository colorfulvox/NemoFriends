from django.db import models

# Create your models here.
class Animal(models.Model):
    species = models.TextField()
    feeds = models.JSONField(defalut={})
    characteristics = models.JSONField(default={})
    commands = models.JSONField(default={})
    default_color = models.IntegerField()
