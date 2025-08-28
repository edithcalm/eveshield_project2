from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()

# Create User serializer class


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'username', 'email', 'password']
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": False, "allow_blank": True, "allow_null": True}
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'username', 'email', 'password']
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": False, "allow_blank": True, "allow_null": True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    """
    Serializer class to authenticate users with phone_number and password.
    """
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
