from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Animal(models.Model):
    species = models.TextField()
    feeds = models.JSONField(default=list)
    characteristics = models.JSONField(default=list)
    commands = models.JSONField(default=list)
    default_color = models.IntegerField()
    # host_users = models.ManyToManyField(User, through='User_Animal', related_name='guest_animals')
    
    def __str__(self):
        return self.species

class User_Animal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    exp = models.IntegerField(default=0)
    is_located = models.BooleanField(default=False)
    color_id = models.IntegerField()
    talking_cnt = models.IntegerField(default=0)
    playing_cnt = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    last_eating_time = models.DateTimeField()
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name
