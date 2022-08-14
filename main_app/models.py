from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    participants = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
