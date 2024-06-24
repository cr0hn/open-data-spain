from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


# -------------------------------------------------------------------------
# Generic response serializers
# -------------------------------------------------------------------------
class ResponseMessageSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="response message")


# -------------------------------------------------------------------------
# Create user serializers
# -------------------------------------------------------------------------
class RequestCreateAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['role'] = get_user_model().UserRoles.ADMIN
        validated_data['is_staff'] = True

        return get_user_model().objects.create_user(**validated_data)


# -------------------------------------------------------------------------
# Login serializers
# -------------------------------------------------------------------------
class ResponseLoginSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="ok")
    refresh = serializers.CharField(help_text="Refresh token")
    access = serializers.CharField(help_text="Access token")


class RequestLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid username/password. Please try again!")

        if not (user.is_staff or user.is_superuser):
            raise serializers.ValidationError("Not enough privileges to login with username/password")

        return user


__all__ = ("RequestCreateAdminUserSerializer", "RequestLoginSerializer", "ResponseLoginSerializer", "ResponseMessageSerializer")
