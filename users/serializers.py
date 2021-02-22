from datetime import datetime, timezone

from django.db.utils import IntegrityError

from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            'phone', 'first_name', 'last_name', 'email', 'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'phone', 'first_name', 'last_name', 'email',
        )
        read_only_fields = ('id', 'phone', 'first_name', 'last_name', 'email')
