from django.db import models
from django.utils import timezone

class UserInfo(models.Model):
    Name = models.CharField(max_length=100)
    Class = models.CharField(max_length=30)

    Father_Name = models.CharField(max_length=100)
    Mother_Name = models.CharField(max_length=100)
    Phone_no = models.CharField(max_length=10)
    email = models.EmailField(unique=True, null=True, blank=True)
    Profile_pic=models.ImageField(upload_to='profiles/',blank=True,null=True)

    password=models.CharField(max_length=200)
    logged_in = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
