from typing import Any, Dict
from django.contrib.auth.models import User
import json
from rest_framework import serializers
from .models import Profile, Avatar
from drf_spectacular.utils import extend_schema, extend_schema_view, extend_schema_field
from drf_spectacular.openapi import OpenApiTypes, OpenApiParameter
from rest_framework.request import Request
from django.http.request import QueryDict

class SignInSerializer(serializers.ModelSerializer):
    """
    Сериалайзер обрабатываеющий данные для входа пользователя на сайт
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def to_internal_value(self, data: Any) -> dict:
        cleaned_data = json.loads(list(data)[0])
        return cleaned_data


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериалайзер обрабатываеющий данные по регистрации пользователя
    """
    first_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password')

    def to_internal_value(self, data: QueryDict) -> Dict[str, str]:
        cleaned_data = json.loads(list(data)[0])
        cleaned_data['first_name'] = cleaned_data['name']
        del cleaned_data['name']
        return cleaned_data

    def validate(self, data):
        """
        Validate both password and username.
        """
        password = data.get('password')
        username = data.get('username')

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        existing_username = User.objects.filter(username=username).exists()
        if existing_username:
            raise serializers.ValidationError("Username must be unique.")

        return data


class AvatarSerializer(serializers.ModelSerializer):
    """
    Сериалайзер обрабатывающий данные аватара пользователя
    """
    class Meta:
        model = Avatar
        fields = ('image', 'alt', 'src')
    src = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()

    @staticmethod
    def get_src(obj) -> str:
        if obj.image:
            return obj.image.url
        return None

    @staticmethod
    def get_alt(obj) -> str:
        if obj.image:
            return obj.image.name
        return None


class ProfileGetPostSerializer(serializers.ModelSerializer):
    """
    Сериалайзер обрабатывающий данные профиля пользователя
    как на сохранение в базе данных так и на выдачу из нее
    """
    avatar = AvatarSerializer(source='avatar_image', read_only=True)#

    class Meta:
        model = Profile
        fields = ('fullName', 'phone', 'email', 'avatar')

    fullName = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)

    def update(self, instance: Profile, validated_data: dict) -> Dict[str, str]:
        instance.email = validated_data.get('email', instance.email)
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class PasswordSerializer(serializers.Serializer):
    currentPassword = serializers.CharField(max_length=10)
    newPassword = serializers.CharField(max_length=10)
