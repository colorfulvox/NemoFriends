from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=64, primary_key=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    name = models.CharField(max_length=16, default=" ")
    gold = models.IntegerField(default=0)
    bgm = models.IntegerField(default=50)
    effect = models.IntegerField(default=50)
    is_called = models.BooleanField(default=False)
    exp_cnt = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
        
class WordChain(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    score = models.IntegerField(default=0)
    words = models.JSONField()