from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


ROLE_CHOICES = [
    ('executing_agency_limit', 'executing_agency_limit'),
    ('location_limit', 'location_limit'),
    ('yearly_funding', 'yearly_funding'),
]


class Constraint(models.Model):
    code = models.CharField( max_length=128)
    max_limit = models.CharField( max_length=128)
    constraint_type = models.CharField(max_length=128, choices=ROLE_CHOICES)
    def __str__(self):
        return f"{self.code} {self.max_limit} {self.constraint_type}"
