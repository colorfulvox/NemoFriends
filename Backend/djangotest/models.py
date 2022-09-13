from django.db import models

# Create your models here.
class Test(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    success = models.CharField(max_length=20, default="Success!!")

class ArrayTest(models.Model):
    column = models.JSONField(default='{}')