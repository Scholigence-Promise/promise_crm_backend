from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    #Email uniqueness validation
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    #Create User + CustomUser
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],  # required
            email=validated_data['email'],
            password=validated_data['password']
        )
        CustomUser.objects.create(user=user)
        return user