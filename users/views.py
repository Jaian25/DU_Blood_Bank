from django.shortcuts import render
from rest_framework.response import Response
from .models import User, Donations
from .serializers import UserSerializer, DonationsSerializer
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
    def patch(self, request, pk=None, format=None):
        print(request.user.id)

        user = request.user
        stu = User.objects.get(pk=user.id)
        print(user.id)
        serializer = UserSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UsersUtilAPI(GenericAPIView):
    def get(self, request):
        # print(request.query_params)
        dt = dict(request.query_params )
        print(dt)
        stu = User.objects.all()
        
        stu = User.objects.filter(area__in = dt['area'])
        serializer = UserSerializer(stu, many=True)
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
        # print("hereeeee")
        print(request.data.keys())
        if ('day' in request.data.keys()) and ('month' in request.data.keys()) and ('year' in request.data.keys()):
            try:
                
                yymmdd = f"{request.data['year']}-{request.data['month']}-{request.data['day']}"
                request.data['last_donated'] = yymmdd
            except:
                request.data['last_donated'] = None
        else:
            request.data['last_donated'] = None
        serializer = UserSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)
        else:
           
            ers = {}
            for keys in serializer.errors.keys():
                val = ''
                for i in range(len(serializer.errors[keys])):
                    val = f'{val}{serializer.errors[keys][i]}'
                ers[keys] = val


        return Response(ers, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        permission_classes = (permissions.IsAuthenticated,)
        authentication_classes = [TokenAuthentication, ]
        print(request.user.id)
        id = pk
        stu = User.objects.get(pk=id)
        print('id')
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




class DonationsAPI(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            donation = DonationsSerializer.objects.get(id=id)
            serializer = DonationsSerializer(donation)
            return Response({'data': serializer.data, 'success': True})
        review = Donations.objects.all()            
        serializer = DonationsSerializer(review, many=True)
        return Response({'data': serializer.data, 'success': True})

    def post(self, request, format=None):
       
        review_data = {'user_id': request.user.id,  'review': request.data['review'], 'date': request.data['date']}
        print(review_data)
        serializer = DonationsSerializer(data=review_data)
        if serializer.is_valid():
            obj = serializer.save()                
            return Response({'msg': 'Data Created','success': True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        id = pk
        data = Donations.objects.get(pk=id)
        serializer = DonationsSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Partial Data Updated'})
        return Response(serializer.errors)