from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "confirm_password"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True}
        }


    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if bool(re.match(pattern, email)):
            return email
        return False
    
    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("confirm_password")
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
    def create(self, validated_data):
        email = validated_data["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address is already registered.")
        
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=26)
    

    class Meta:
        model = User
        fields = ['email', 'password']

