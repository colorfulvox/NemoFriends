from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Decoration(models.Model):
    id = models.AutoField(primary_key=True)
    cost = models.IntegerField()
    is_rare = models.BooleanField()

    def __str__(self):
        return f'{self.id}번 조경'


class User_Decoration(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    decoration = models.ForeignKey(Decoration, on_delete=models.CASCADE)
    is_located = models.BooleanField()
    location = models.IntegerField(blank=True, null=True)
    angle = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}의 {self.decoration.id}번 조경'


class Item(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{self.id}번 염색약'


class User_Item(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cnt = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.user}의 {self.id}번 염색약'