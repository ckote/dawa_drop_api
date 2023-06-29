from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import BadRequest
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED
import requests
from awards.serializers import RedemptionSerializer, PatientProgramEnrollmentSerializer
from core import permisions as custom_permissions
from rest_framework import permissions, status
from urllib.parse import parse_qs
from core.exceptions import PatientNotFoundException, OperationNotPermittedException
from core.mixin import PatientDetailsSyncMixin
from patients.mixins.sync import PatientSyncMixin
from users.api import search_patient
from users.models import Patient, AccountVerification
from users.serializers import (
    UserProfileSerializer, UserLoginSerializer,
    UserCredentialSerializer, UserRegistrationSerializer, UserInformationViewSerializer, ProfileSerializer,
    AccountSearchSerializer, AccountVerifySerializer, AccountSearchResultSerializer
)
from users.utils import obscure_email, obscure_number, update_patient
from django.db.models import Q


class DoctorsMixin:
    @action(detail=False, url_name='doctor-list', url_path='doctors')
    def doctors_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(profile__user_type='doctor')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PatientsMixin:
    @action(
        detail=False, url_name='patient-list', url_path='patients',
        permission_classes=[custom_permissions.IsAgentOrDoctor]
    )
    def patients_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(profile__user_type='patient')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AgentsMixin:
    @action(detail=False, url_name='agent-list', url_path='agents')
    def agents_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(profile__user_type='agent')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, url_name='agent-detail', permission_classes=[permissions.IsAuthenticated])
    def agent_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AuthMixin:

    @action(
        methods=['post'],
        url_path='change-password',
        detail=False,
        url_name='change_password',
        description="Change current User password",
        permission_classes=[
            permissions.IsAuthenticated
        ],
        serializer_class=UserCredentialSerializer
    )
    def change_password(self, request, *args, **kwargs):
        """
        Simply works as view function on view methods
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'changed': True})

    @action(
        methods=['post'],
        description="Supports user registration system",
        detail=False,
        url_name='register',
        url_path='register',
        serializer_class=UserRegistrationSerializer,
        permission_classes=[
            permissions.AllowAny
        ],
    )
    def register(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = UserInformationViewSerializer(instance=user, context={'request': request}).data
            data.update({'token': token.key})
            return Response(
                data,
                status=HTTP_201_CREATED
            )

    @action(
        methods=['post'],
        description='User Login View',
        detail=False,
        url_path='login',
        url_name='login',
        serializer_class=UserLoginSerializer,
        permission_classes=[
            permissions.AllowAny
        ],
    )
    def login(self, request, *args, **kwargs):
        _serializers = UserLoginSerializer(data=request.data)
        if _serializers.is_valid(raise_exception=True):
            username = _serializers.validated_data.get("username")
            password = _serializers.validated_data.get("password")
            user = authenticate(
                username=username,
                password=password
            )
            if not user:
                return Response({
                    'username': [''],
                    'password': ['Invalid Username or password'],
                },
                    status=400)
            token, created = Token.objects.get_or_create(user=user)
            data = UserInformationViewSerializer(instance=user, context={'request': request}).data
            data.update({'token': token.key})
            return Response(data)


class ProfileMixin(PatientDetailsSyncMixin):
    @action(
        methods=['put', 'get'],
        description='User profile',
        detail=False,
        permission_classes=[
            permissions.IsAuthenticated
        ],
        # authentication_classes=[TokenAuthentication, BasicAuthentication],
        serializer_class=UserProfileSerializer
    )
    def profile(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data, instance=user)
        if request.method == 'PUT':
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
        return Response(self.get_serializer(instance=user).data)

    @action(
        methods=['put', 'get'],
        description='User profile',
        detail=True,
        permission_classes=[
            permissions.IsAuthenticated
        ],
        serializer_class=ProfileSerializer
    )
    def profile_detail(self, request, *args, **kwargs):
        user = request.user.profile
        serializer = self.get_serializer(data=request.data, instance=user)
        if request.method == 'PUT':
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
        return Response(self.get_serializer(instance=user).data)

    @action(
        methods=['get'],
        description='User profile view',
        detail=False,
        permission_classes=[
            permissions.IsAuthenticated
        ],
        url_name='profile-view',
        url_path='profile-view',
        serializer_class=UserInformationViewSerializer)
    def profile_view(self, request, *args, **kwargs):
        user = request.user
        return Response(self.get_serializer(instance=user).data)

    def is_valid(self, account):
        from .api import get_patient_by_uuid
        # Check if patient exist remote if not raise error
        if get_patient_by_uuid(account) is None:
            raise PatientNotFoundException()
        # Check if exist locally and is linked , if yes rase error
        patients = Patient.objects.filter(uuid=account)
        if patients.exists() and patients.first().user:
            raise OperationNotPermittedException(detail='User with search account already exist')

    @action(
        methods=['post'], url_name='find-account', url_path='find-account', detail=False,
        serializer_class=AccountSearchSerializer, permission_classes=[
            permissions.IsAuthenticated, custom_permissions.IsPatient,
            custom_permissions.HasNoRelatedUserType], )
    def find_my_account(self, request, *args, **kwargs):
        """Find patient account with patient number or national id"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        search_param = serializer.validated_data.get('search')
        """if search_param:
                    patients = Patient.objects.filter(
                        Q(patient_number__contains=search_param) |
                        Q(national_id__contains=search_param)
                    )  # .only('patient_number', 'email', 'phone_number')
                    page = self.paginate_queryset(patients)
                    if page is not None:
                        paginated = AccountSearchResultSerializer(
                            page,
                            many=True,
                            context={'request': request}
                        )
                        return self.get_paginated_response(paginated.data)
                    paginated = self.get_serializer(patients, many=True)
                    return Response(paginated.data)
                return Response({'search': search_param, 'results': []})"""

        resp = self.find_remote_patient(search_param, request)
        return Response({'results': resp})

    def find_remote_patient(self, upi, request):
        patients = search_patient(upi, request)
        return patients

    @action(
        methods=['get'], url_name='request-verification', url_path='verify-request', detail=False,
        permission_classes=[permissions.IsAuthenticated, custom_permissions.IsPatient,
                            custom_permissions.HasNoRelatedUserType])
    def request_verification(self, request, *args, **kwargs):
        from .api import get_phone_number, get_patient_by_uuid
        account = request.GET.get("account")
        # validate query strong
        self.is_valid(account)
        # create verification object
        AccountVerification.objects.create(
            user=request.user,
            search_value=account
        )
        data = {
            'verify_url': reverse(
                viewname='users:user-verify',
                request=request
            ),
            'message': f"Check your phone number {obscure_number(get_phone_number(get_patient_by_uuid(account)['person']['attributes']))} for verification code"
        }
        return Response(data=data)

    @action(
        methods=['post'], url_name='verify', url_path='verify', detail=False,
        serializer_class=AccountVerifySerializer,
        permission_classes=[permissions.IsAuthenticated, custom_permissions.IsPatient,
                            custom_permissions.HasNoRelatedUserType], )
    def account_verification(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        verification = AccountVerification.objects.get(
            code=code,
            user=request.user,
            is_verified=False
        )
        account = verification.search_value
        patient = self.get_or_create_patient(account)
        self.sync(patient)
        patient.user = request.user
        patient.save()
        verification.is_verified = True
        verification.save()
        return Response(data={"detail": "Account verification successful"}, status=status.HTTP_200_OK)

    @action(
        methods=['get'], url_name='pre-fill-details', url_path='pre-fill-details', detail=False,
        permission_classes=[permissions.IsAuthenticated, custom_permissions.IsPatient,
                            custom_permissions.HasRelatedUserType], )
    def prefill_details(self, request, *args, **kwargs):
        patient = request.user.patient
        user = request.user
        profile = user.profile

        user.first_name = patient.first_name
        user.last_name = patient.last_name
        if patient.email:
            user.email = patient.email
        user.save()

        profile.gender = patient.gender
        profile.phone_number = patient.phone_number
        profile.save()

        return Response(data={'detail': 'Account details update successfully'})


class DoctorNextOfKeenMixin:
    @action(detail=True)
    def next_of_keen(self, request, *args, **kwargs):
        pass
