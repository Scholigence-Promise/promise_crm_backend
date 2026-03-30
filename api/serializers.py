from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser,Profile

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
    
    
    


# 🔸 User Serializer (Nested)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# 🔸 Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  

    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'bio', 'profile_pic', 'role']

    def validate(self, data):
        user_data = data.get('user')
    
        if user_data:
            username = user_data.get('username')

        # Exclude current user during update
            if User.objects.filter(username=username).exclude(id=self.instance.user.id if self.instance else None).exists():
                raise serializers.ValidationError("Username already exists.")
    
        return data

    # 🔹 Field Validations
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value

    def validate_bio(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Bio cannot exceed 500 characters.")
        return value

    # 🔹 Create Profile with Nested User
    def create(self, validated_data):
        user_data = validated_data.pop('user')

        user = User.objects.create(
            username=user_data['username'],
            email=user_data.get('email', '')
        )

        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    # 🔹 Update Profile with Nested User
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Update user data if provided
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()

        # Update profile fields
        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.role = validated_data.get('role', instance.role)
        instance.save()

        return instance