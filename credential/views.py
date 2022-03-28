"""This module is used to
do the operations on credentials
"""
from django.http import HttpRequest
from django.http import HttpResponse

from django.db import DatabaseError
from django.db import IntegrityError
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response

from credential.serializer import CredentialSerializer
from credential.serializer import CredentialDetailsSerializer
from credential.serializer import AccessibleUserSerializer

from credential.models import Credential
from credential.models import CredentialDetails
from credential.models import AccessibleUser


@api_view(['GET', 'POST', 'PUT'])
def do_credentials(request: HttpRequest):
    if request.method == 'GET':
        return get_credentials(request)

    if request.method == 'POST':
        return create_credential(request)

    if request.method == 'PUT':
        return update_credential(request)


@api_view(['GET', 'POST', 'DELETE'])
def do_credential_details(request: HttpRequest, credential_id):
    if request.method == 'GET':
        return get_accessible_credential_details(request, credential_id)

    if request.method == 'POST':
        return create_user_access(request, credential_id)

    if request.method == 'DELETE':
        return remove_user_access(request, credential_id)


def create_credential(request):
    try:
        with transaction.atomic():
            credential_dict = request.data
            credential_details_list_dict = credential_dict \
                .pop('credential_details_list')
            credential = Credential.objects.create(**credential_dict)

            credential_details_list = []

            for credential_details in credential_details_list_dict:
                credential_details_list \
                    .append(CredentialDetails(**credential_details,
                                              credential=credential))

            credential_details_list = CredentialDetails.objects \
                .bulk_create(credential_details_list)

            credential_serializer = CredentialSerializer(credential)
            credential_details_serializer \
                = CredentialDetailsSerializer(credential_details_list,
                                              many=True)
            return HttpResponse('created')
    except DatabaseError:
        return HttpResponse('Credential creation failed')


def get_credentials(request):
    credentials = Credential.objects.all()
    serializer = CredentialSerializer(credentials, many=True)
    return Response(serializer.data)


def update_credential(request):
    try:
        with transaction.atomic():
            credential_dict = request.data
            credential_details_list_dict = credential_dict \
                .pop('credential_details_list')
            credential = Credential(**credential_dict)
            credential.save()

            credential_details_list = []

            for credential_details in credential_details_list_dict:
                credential_details = CredentialDetails(**credential_details,
                                                       credential=credential)
                credential_details.save()
                credential_details_list.append(credential_details)

            credential_details_list = CredentialDetailsSerializer(
                credential_details_list,
                many=True
            )

            serializer = CredentialSerializer(credential)
            return Response(serializer.data)
    except DatabaseError:
        return HttpResponse('Credential update failed')


def create_user_access(request, credential_id):
    email_address = request.data.get('email')

    try:
        accessible_user = AccessibleUser.objects \
            .create(employee_id=email_address,
                    credential_id=credential_id)
        serializer = AccessibleUserSerializer(accessible_user)
        return Response(serializer.data)
    except IntegrityError:
        return HttpResponse('You have access already')


def get_accessible_credential_details(request, credential_id):
    email_address = request.GET['email']

    accessible_users = AccessibleUser.objects \
        .filter(credential_id=credential_id,
                employee_id=email_address)

    if len(accessible_users) > 0:
        credential_details = CredentialDetails.objects \
            .filter(credential_id=credential_id)
        serializer = CredentialDetailsSerializer(credential_details, many=True)
        return Response(serializer.data)
    else:
        return HttpResponse('You don\'t have access for this credential')


def remove_user_access(request, credential_id):
    email_address = request.data.get('email')
    accessible_users = AccessibleUser.objects \
        .filter(credential_id=credential_id,
                employee_id=email_address)

    if len(accessible_users) > 0:
        accessible_users.delete()
        return HttpResponse('Access removed')
    else:
        return HttpResponse('No such credentials was allocated')
