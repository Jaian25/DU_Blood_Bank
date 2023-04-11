from django.shortcuts import render
from rest_framework.response import Response
from .models import User, Review
from .serializers import UserSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView

class CurrentUserAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        print(request.user)
        user = request.user
        serializer = UserSerializer(user)
        return Response({'data': serializer.data, 'success': True})


class UsersAPI(GenericAPIView):
    
    
    def get(self, request, pk=None, format=None):
        
        # test = {"name" : "jaian" , "age" : "18"}
        # return Response(test)
        
        id = pk
        if id is not None:
            stu = User.objects.get(id=id)
            serializer = UserSerializer(stu)
            
            dt = serializer.data
            # del dt['password']
            print(dt['password'])
            dt['password'] = 00
            return Response({'data': dt, 'success': True})

        stu = User.objects.all()
        serializer = UserSerializer(stu, many=True)
        # print(serializer.data)
        for user in serializer.data:
            # print(user['password'])
            #user['password']=0
            del user['password']
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        stu = User.objects.get(pk=id)
        serializer = UserSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        id = pk
        stu = User.objects.get(pk=id)
        stu.delete()
        return Response({'msg': 'Data Deleted'})




class ReviewAPI(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            review = ReviewSerializer.objects.get(id=id)
            serializer = ReviewSerializer(review)
            return Response({'data': serializer.data, 'success': True})
        review = Review.objects.all()            
        serializer = ReviewSerializer(review, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
        print(request.data['project_id'])
        review_data = {'user_id': request.user.id, 'project_id': request.data['project_id'], 'review': request.data['review'], 'rating': request.data['rating']}
        serializer = ReviewSerializer(data=review_data)
        if serializer.is_valid():
            obj = serializer.save()                
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Review.objects.get(pk=id)
        serializer = ReviewSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)