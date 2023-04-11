from django.shortcuts import render
from rest_framework.response import Response
from .models import Agency,Project , Component, Location, ExecutionInterval
from constraint.models import Constraint
from constraint.serializers import ConstraintSerializer
from .serializers import AgencySerializer, ComponentSerializer, LocationSerializer,ProjectSerializer ,ExecutionIntervaSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.filters import SearchFilter

from .utils import calculate_end_time

from rest_framework.decorators import api_view
import csv
# from django_filters.rest_framework import DjangoFilterBackend
class ProjectAPI(APIView):    
    # pass
    # filter_backends = [SearchFilter]
    # search_fields = ['project_name' ] 
    
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]   


    def get(self, request, pk=None, format=None):
        
        # test = {"name" : "jaian" , "age" : "18"}
        # return Response(test)
        # print(request.query_params.get('category'))
        # category = request.query_params.get('category')
        project_name= request.query_params.get('project_name')
        exec= request.query_params.get('exec')
        status = request.query_params.get('status')
        my_projects = request.query_params.get('my_projects')


        # print(status)
        # project_start_time= request.query_params.get('project_start_time')
        # project_completion_time= request.query_params.get('categproject_completion_timeory')
        # total_budget= request.query_params.get('total_budget')
        id = pk
        if id is not None:
            project = Project.objects.get(id=id)
            serializer = ProjectSerializer(project)
            return Response({'data': serializer.data, 'success': True})
        projects = Project.objects.all()

        project_objects = ProjectSerializer(Project.objects.exclude(start_date=None), many=True).data
        if my_projects == 'true' and request.user.role == 'exec':
            projects = projects.filter(exec=request.user.agency.id)

        if request.user.role == 'users':
            projects = projects.exclude(start_date=None)

        project_objects = ProjectSerializer(projects, many=True).data
        constraint_objects = ConstraintSerializer(Constraint.objects.all(), many=True).data
        component_objects = ComponentSerializer(Component.objects.all(), many=True).data
        agency_objects = AgencySerializer(Agency.objects.all(), many=True).data

        data = calculate_end_time(project_objects, constraint_objects, component_objects , agency_objects)


        # if category is not None and len(category)>0:
        #     projects = projects.filter(category = category)
        if project_name is not None and len(project_name)>0:
            projects = projects.filter(project_name__icontains=project_name)
        if exec is not None and int(exec)>0:
            projects = projects.filter(exec = int(exec))
        
        if status is not None and len(status)>0:
            # print(status, "here")
            if status == 'running':
                projects = projects.exclude(start_date=None)
            elif status == 'not_started':
                projects = projects.filter(start_date=None)
        # if project_completion_time is not None and len(project_completion_time)>0:
        #     projects = projects.filter(project_completion_time = project_completion_time)
        # if total_budget is not None and len(total_budget)>0:
        #     projects = projects.filter(total_budget = total_budget)
        
            
        serializer = ProjectSerializer(projects, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        location = request.data['location']
        loc, created = Location.objects.get_or_create(name = location)
        request.data['location'] = loc.id
        request.data['exec'] = request.user.agency.id

        print(request.data)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = Project.objects.get(pk=id)
        location = request.data['location']

        loc, created = Location.objects.get_or_create(name = location)
        request.data['location'] = loc.id
        serializer = ProjectSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated','success': True})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        stu = Project.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'})

class AgencyAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            agency = Agency.objects.get(id=id)
            serializer = AgencySerializer(agency)
            return Response({'data': serializer.data, 'success': True})
        agency = Agency.objects.all()            
        serializer = AgencySerializer(agency, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
            
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()                
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Agency.objects.get(pk=id)
        serializer = AgencySerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)



class ComponentAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            component = Component.objects.get(id=id)
            serializer = ComponentSerializer(component)
            return Response({'data': serializer.data, 'success': True})
        component = Component.objects.all()            
        serializer = ComponentSerializer(component, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
            
        serializer = ComponentSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()                
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Component.objects.get(pk=id)
        serializer = ComponentSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

class LocationAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            project = Location.objects.get(id=id)
            serializer = LocationSerializer(project)
            return Response({'data': serializer.data, 'success': True})
        locations = Location.objects.all()            
        serializer = LocationSerializer(locations, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
            
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()                
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Location.objects.get(pk=id)
        serializer = LocationSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

class ExectionIntervalAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            project = ExecutionInterval.objects.get(id=id)
            serializer = ExecutionIntervaSerializer(project)
            return Response({'data': serializer.data, 'success': True})
        executionIntervals = ExecutionInterval.objects.all()            
        serializer = ExecutionIntervaSerializer(executionIntervals, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
            
        serializer = ExecutionIntervaSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()                
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = ExecutionInterval.objects.get(pk=id)
        serializer = ExecutionIntervaSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)


@api_view(['GET'])
def load_data(request):
    Agency.objects.all().delete()
    Project.objects.all().delete()
    Constraint.objects.all().delete()
    Component.objects.all().delete()

    f = open('data/agencies.csv', 'r')
    agencies = csv.reader(f)
    flag = False
    for row in agencies:
        if flag is False:
            flag = True 
            continue
        Agency.objects.create(code = row[0] , name = row[1] , type = row[2], description = row[3])


    f = open('data/projects.csv' , 'r')
    projects = csv.reader(f)
    flag = False
    for row in projects:
        if flag is False:
            flag = True 
            continue
        loc, created = Location.objects.get_or_create(name = row[1])
        exec_pk = Agency.objects.get(code = row[4])

 
        
        Project.objects.create(project_name = row[0] , location = loc, latitude = row[2] , longitude = row[3],
            exec = exec_pk , cost = row[5] , timespan = row[6], project_id = row[7], goal = row[8],
            start_date = row[9], completion = row[10] , actual_cost = row[11], status ='running'
        )

    f = open('data/proposals.csv' , 'r')
    projects = csv.reader(f)
    flag = False
    for row in projects:
        if flag is False:
            flag = True 
            continue
        loc, created = Location.objects.get_or_create(name = row[1])
        exec_pk = Agency.objects.get(code = row[4])
        Project.objects.create(project_name = row[0] , location = loc, latitude = row[2] , longitude = row[3],
            exec = exec_pk , cost = row[5] , timespan = row[6], project_id = row[7], goal = row[8],
            start_date = None, completion = None, proposal_date=row[9] , status = 'not started'
        )

    f = open('data/components.csv' , 'r')
    components = csv.reader(f)
    flag = False
    for row in components:
        if flag is False:
            flag = True 
            continue
        project_pk = Project.objects.get(project_id = row[0])
        try:
            depends_on = Component.objects.get(component_id=row[4])
        except:
            depends_on = None
        
        Component.objects.create(project = project_pk, component_id = row[2] , component_type = row[3], depends_on = depends_on, budget_ratio=row[5])

    f = open('data/constraints.csv' , 'r')
    constraints = csv.reader(f)
    flag = False
    for row in constraints:
        if flag is False:
            flag = True 
            continue 
        _code = row[0]
        _limit = row[1]
        _type = row[2]     
        if _type == 'executing_agency_limit':
            Agency.objects.filter(code=_code).update(max_component_limit = _limit)
        if _type == 'yearly_funding':
            Agency.objects.filter(code=_code).update(max_budget_limit = _limit)
        if _type == 'location_limit':
            Location.objects.filter(name = _code).update(max_limit = _limit)
        Constraint.objects.create(code = row[0], max_limit = row[1] , constraint_type = row[2])


    return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)


