from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'password',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # La contraseña no debe aparecer en las respuestas
        }

    def create(self, validated_data):
        # Hashea la contraseña antes de guardar el usuario
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)