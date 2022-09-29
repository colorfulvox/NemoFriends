from django.db import models

from django.contrib.auth.models import AbstractUser

from animals.models import Animal

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=64, primary_key=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    gold = models.IntegerField(default=0)
    bgm = models.IntegerField(default=50)
    effect = models.IntegerField(default=50)
    is_called = models.BooleanField(default=False)
    exp_cnt = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username


class Mbti(models.Model):
    mbti = models.CharField(primary_key=True, max_length=4)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.mbti + ":" + self.animal.species
