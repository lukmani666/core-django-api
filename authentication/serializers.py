from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.core import exceptions
from django.contrib.auth import authenticate

class SignUpUserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    confirm_password = serializers.CharField(write_only=True, max_length=30)
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "phone",
            "email",
            "password",
            "confirm_password",
            "date_joined",
            "is_verified",
            "token",
        ]

        extra_kwargs = {
            "password": {"write_only": True}
        }

        read_only_fields = ["id", "token", "date_joined","is_verified"]

    def validate(self, data):
        errors = {}
        confirm_password = data.get("confirm_password", "")
        password = data.get("password", "")
        email = data.get("email", "")
        if password.lower() != confirm_password.lower():
           errors["password"] = ["Password must match"]
        try:
            validate_password(password=password) and validate_password(
                password=confirm_password
            )
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
        
        email_ = User.objects.filter(email__iexact=email)
        if email_.exists():
            errors["email"] = ["Email already exists"]

        if errors:
            raise serializers.ValidationError(errors)
        
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        self.token = token.key
        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(self, "token"):
            data["token"] = self.token
        return data
    

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=20)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if not email and not password:
            raise serializers.ValidationError("Email and password are required")
        
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email does not exits")
        
        
        if not user.check_password(password):
            raise serializers.ValidationError("Password not correct")
        
        user = authenticate(email=user.email, password=password)
        if not user:
            raise serializers.ValidationError("Authentication failed")
        
        token, created = Token.objects.get_or_create(user=user)

        data["token"] = token.key
        data["user"] = user
        return data
    
        