from rest_framework import serializers

from .models import Agency,Project,Component,Location,ExecutionInterval
from users.models import Review
from users.serializers import ReviewSerializer

import datetime
import time

class ProjectSerializer(serializers.ModelSerializer):
    
    location_name = serializers.SerializerMethodField(read_only = True)
    exec_name = serializers.SerializerMethodField(read_only = True)
    reviews = serializers.SerializerMethodField(read_only = True)
    # status = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Project
        fields = ['id' , 'project_name' , 'location' , 'location_name', 'exec_name', 'latitude' , 'longitude' , 'reviews', 'exec' , 'cost' , 'timespan' , 'project_id' , 'goal' , 'start_date' , 'completion', 'actual_cost', 'proposal_date', 'status']
    
    def get_location_name(self, obj):
        return obj.location.name
    def get_exec_name(self, obj):
        return obj.exec.code
    def get_reviews(self, obj):
        return ReviewSerializer(Review.objects.filter(project_id=obj.id), many=True).data
    # def get_status(self, obj):
    #     if obj.start_date == None:
    #         return 'Not Started'
    #     return 'Running'
        
class AgencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Agency
        fields = ['id', 'code', 'name', 'type', 'description','max_budget_limit','max_component_limit']

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Component 
        fields = ['id' , 'project', 'component_id', 'component_type', 'depends_on', 'budget_ratio']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id' , 'name' , 'max_limit']

class ExecutionIntervaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id' , 'project_id','name' , 'from_date', 'to_date']

