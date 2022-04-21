from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PassManager(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)


class SharingDetails(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver = models.IntegerField()
    edit_access = models.BooleanField(default=0)
