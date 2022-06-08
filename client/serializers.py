from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from client.models import Client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

    # override create method for hashing password of an client
    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')

        client = Client.objects.create(name=name, email=email, active=True)

        client.password = make_password(validated_data.get('password'))
        client.save()

        return client
