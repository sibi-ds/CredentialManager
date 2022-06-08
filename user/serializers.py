from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'active',
                  'created_at', 'created_by', 'updated_at', 'updated_by', ]

    # override create method for hashing password of an employee
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')

        user = User.objects.create(name=name, email=email, active=True)

        user.password = make_password(validated_data.get('password'))
        user.save()

        return user
