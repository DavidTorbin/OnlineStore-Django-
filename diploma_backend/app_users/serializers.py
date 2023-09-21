from rest_framework import serializers
from django.contrib.auth.models import User

from app_users.models import UserProfile, Payments


class UserSerializer(serializers.Serializer):
    fullName = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=12)
    avatar = serializers.CharField()

    def update(self, instance, validated_data):
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        return instance


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, required=True)


class AvatarUpdateSerializer(serializers.Serializer):
    url = serializers.CharField()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['number', 'name', 'month', 'year', 'code']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['month'] = int(repr['month'])
        repr['year'] = int(repr['year'])
        repr['code'] = int(repr['code'])
        return repr

