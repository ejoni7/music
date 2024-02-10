from django.http import HttpResponse
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    """override create method to change the password into hash."""

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(SignupSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ['phone', 'username', 'password']


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['phone', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True, )
    new_password = serializers.CharField(required=True)


class ForgetPasswordSerializer(serializers.Serializer):
    number = serializers.IntegerField(max_value=9999999999, min_value=9000000000)
    username = serializers.CharField(max_length=40)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio', 'image', ]
