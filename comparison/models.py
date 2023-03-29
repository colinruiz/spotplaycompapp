from django.db import models

# Create your models here.

class MyData(models.Model):
    playlist_id = models.CharField(max_length= 100)
    #playlist_id_2 = models.CharField(max_length=100)
    
class Second(models.Model):
    playlist_id = models.CharField(max_length=100)


# from django.db import models

# # Create your models here.

# class Dropdown(models.Model):
#     user_input = models.CharField(max_length=100)
