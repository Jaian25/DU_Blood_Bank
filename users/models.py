from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import datetime
# from project.models import Agency, Project

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=64)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    blood_type = models.CharField(max_length=64, null=True, blank=True)
    area = models.CharField(max_length=64, null=True, blank=True)
    # is_active = models.BooleanField(default=True)
    last_donated = models.DateField(default=datetime.date(1997, 10, 19), null=True)
    number_of_donations =  models.DecimalField(default= 0, decimal_places=0 , max_digits=20)
    phone = models.CharField(max_length=64,null=True, unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username


class Donations(models.Model):
    review = models.CharField(max_length = 1024)
    user_id = models.ForeignKey(User , on_delete = models.CASCADE)
    date = models.DateField(default=datetime.date(1997, 10, 19), null=True)

    def __str__(self):
        return f"{self.user_id} {self.date}"
