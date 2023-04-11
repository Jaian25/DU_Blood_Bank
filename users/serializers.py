from rest_framework import serializers

from .models import User , Review


class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name' , 'password','blood_type'  ]

    # def validate(self, attr):
    #     validate_password(attr['password'])
    #     return attr


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            blood_type = validated_data['blood_type'],
           # last_donated = validated_data['last_donated']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only = True)
    project_name = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Review
        fields = ['id' ,'user_id','project_id', 'review' , 'rating', 'user_name', 'project_name']

    def get_user_name(self, obj):
        return obj.user_id.username
    def get_project_name(self, obj):
        return obj.project_id.project_name