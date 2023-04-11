from django.shortcuts import render
from rest_framework.response import Response
from .models import Constraint
from .serializers import ConstraintSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView



class ConstraintAPI(GenericAPIView):
    
    
    def get(self, request, pk=None, format=None):
        
        # test = {"name" : "jaian" , "age" : "18"}
        # return Response(test)
        
        id = pk
        if id is not None:
            query = Constraint.objects.get(id=id)
            serializer = ConstraintSerializer(query)
            return Response({'data': serializer.data, 'success': True})

        query = Constraint.objects.all()
        serializer = ConstraintSerializer(query, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        serializer = ConstraintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        query = Constraint.objects.get(pk=id)
        serializer = ConstraintSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated','success': True})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        query = Constraint.objects.get(pk=id)
        query.delete()
        return Response({'msg': 'Data Deleted','success': True})
