from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    # override create method for hashing password of an employee
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')

        user = User.objects.create(name=name, email=email)

        user.set_password(validated_data.get('password'))
        user.save()

        return user
