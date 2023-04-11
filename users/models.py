from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from project.models import Agency, Project

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=64)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    blood_type = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    #last_donated = models.DateTimeField(default=timezone.now, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username


class Review(models.Model):
    review = models.CharField(max_length = 1024)
    rating = models.FloatField(default = 5)
    user_id = models.ForeignKey(User , on_delete = models.CASCADE)
    project_id = models.ForeignKey(Project , on_delete = models.CASCADE)