from rest_framework import serializers
from credential.models import Credential
from credential.models import AccessibleUser
from credential.models import CredentialDetails


class CredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credential
        fields = '__all__'


class CredentialDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialDetails
        fields = '__all__'


class AccessibleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessibleUser
        fields = '__all__'
