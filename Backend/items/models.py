from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Decoration(models.Model):
    id = models.AutoField(primary_key=True)
    cost = models.IntegerField()
    is_rare = models.BooleanField()


class User_Decoration(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decoration = models.ForeignKey(Decoration, on_delete=models.CASCADE)
    is_located = models.BooleanField()
    location = models.IntegerField(blank=True, null=True)
    angle = models.IntegerField(blank=True, null=True)


class Color(models.Model):
    id = models.AutoField(primary_key=True)


class User_Color(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    cnt = models.IntegerField(default=1)