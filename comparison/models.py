from django.db import models

# Create your models here.

class MyData(models.Model):
    playlist_id = models.CharField(max_length= 100)
    
class Second(models.Model):
    playlist_id = models.CharField(max_length=100)

class Dropdown(models.Model):
    user_input = models.CharField(max_length=100)

class Dropdown2(models.Model):
    user_input = models.CharField(max_length=100)