from django.db import models

# Create your models here.

class Dropdown(models.Model):
    user_input = models.CharField(max_length=100)
