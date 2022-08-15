from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Activity(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    participants = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

class Date(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(max_length=1000)
    company = models.CharField(max_length=100)
    activity = models.ManyToManyField(Activity)
    location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
