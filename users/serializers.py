from rest_framework import serializers

from .models import User , Donations


class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name' , 'password','blood_type','area','last_donated','number_of_donations','phone'  ]

    # def validate(self, attr):
    #     validate_password(attr['password'])
    #     return attr


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            blood_type = validated_data['blood_type'],
            area = validated_data['area'],
            last_donated = validated_data['last_donated'],
            number_of_donations = validated_data['number_of_donations'],
            phone = validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

# class ReviewSerializer(serializers.ModelSerializer):
#     user_name = serializers.SerializerMethodField(read_only = True)
#     project_name = serializers.SerializerMethodField(read_only = True)

#     class Meta:
#         model = Review
#         fields = ['id' ,'user_id','project_id', 'review' , 'rating', 'user_name', 'project_name']

#     def get_user_name(self, obj):
#         return obj.user_id.username
#     def get_project_name(self, obj):
#         return obj.project_id.project_name
    

class DonationsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Donations
        fields = ['id' ,'user_id', 'review' , 'name', 'date']

    def get_name(self, obj):
        return obj.user_id.name
