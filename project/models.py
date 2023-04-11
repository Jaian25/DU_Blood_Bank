from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


CATEGORY_CHOICES = [
    ('Education', 'Education'),
    ('Health', 'Health'),
    ('Governance', 'Governance'),
    ('Energy and Mining' , 'Energy and Mining')
]

AGENCY_CHOICES = [
    ('EXEC', 'EXEC'), ('APPROV','APPROV'), ('MOP', 'MOP'),
]

COMPONENT_CHOICES = [
    ('goods', 'goods'),
    ('works', 'works')
]

class Agency(models.Model):
    code = models.CharField(unique=True, max_length=256)
    name = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
    max_budget_limit = models.FloatField(null=True)
    max_component_limit = models.FloatField(null=True)


class Location(models.Model):
    name = models.CharField(max_length = 1024)
    max_limit = models.FloatField(null = True)


class Project(models.Model):
    project_name= models.CharField(max_length=1024)
    project_id = models.CharField(null = True , max_length = 1024)
    latitude = models.FloatField()
    longitude = models.FloatField()
    exec = models.ForeignKey(Agency , on_delete = models.CASCADE)
    location = models.ForeignKey(Location , on_delete = models.CASCADE)
    # location_id = models.ForeignKey()
    goal= models.CharField( max_length=1024)
    start_date = models.DateField(null=True)
    completion = models.FloatField(null=True)
    actual_cost= models.FloatField(default=0)
    proposal_date= models.DateField(null=True, auto_now_add=True)
    status = models.CharField(max_length = 100, null=True)
    cost= models.FloatField()
    timespan= models.FloatField()
    # location,exec,cost,timespan,project_id,goal,start_date,completion,actual_cost
    def __str__(self):
        return self.project_name

class Component(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    component_id = models.CharField(unique = True , max_length = 1024)
    component_type = models.CharField(max_length=1024, choices = COMPONENT_CHOICES)
    depends_on = models.ForeignKey("self", on_delete = models.CASCADE, blank=True, null=True)
    budget_ratio = models.CharField(max_length = 1024)

class ExecutionInterval(models.Model):
    project_id = models.ForeignKey(Project , on_delete = models.CASCADE)
    from_date = models.DateField(null = True)
    to_date = models.DateField( null = True)