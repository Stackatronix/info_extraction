from django.db import models

# Create your models here.
class MyFileUpload(models.Model):    
    my_file=models.FileField()