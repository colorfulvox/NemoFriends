from email.policy import default
from django.db import models
from django.conf import settings
from datetime import datetime
from utils import default
'''
column에 수정 사항이 생기면, admin.py도 변경하기!!
'''

User = settings.AUTH_USER_MODEL


class Animal(models.Model):
    species = models.TextField()
    feeds = models.JSONField(default=list)
    features = models.JSONField(default=list)
    commands = models.JSONField(default=list)
    
    def __str__(self):
        return self.species


class User_Animal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)
    exp = models.IntegerField(default=0)
    is_located = models.BooleanField(default=False)
    talking_cnt = models.IntegerField(default=default['talking_cnt'])
    playing_cnt = models.IntegerField(default=default['playing_cnt'])
    created_at = models.DateField(auto_now_add=True)
    last_eating_time = models.DateTimeField(default=datetime(2022, 9, 1, 0, 0, 0))
    level = models.IntegerField(default=1)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.name