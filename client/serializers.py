from django.contrib.auth.hashers import make_password
from oauth2_provider.models import Application

from rest_framework import serializers

from client.models import Client
from user.models import User


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

    # override create method for hashing password of a client
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')

        client = Client.objects.create(name=name, email=email, active=True)

        client.password = make_password(validated_data.get('password'))
        client.save()

        return client


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = '__all__'
