from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import BadRequest
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED
import requests
from awards.serializers import RedemptionSerializer, PatientProgramEnrollmentSerializer
from core import permisions as custom_permissions
from rest_framework import permissions, status
from urllib.parse import parse_qs

from core.exceptions import VerificationException
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


class ProfileMixin:
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
        if not Patient.objects.filter(patient_number=account).exists():
            # todo rais proper error
            raise BadRequest("Account ain't valid")
        return Patient.objects.get(patient_number=account)

    @action(
        methods=['post'], url_name='find-account', url_path='find-account', detail=False,
        serializer_class=AccountSearchSerializer, permission_classes=[
            permissions.IsAuthenticated, custom_permissions.IsPatient,
            custom_permissions.HasNoRelatedUserType], )
    def find_my_account_and_verify(self, request, *args, **kwargs):
        """Find patient account with patient number or national id"""
        # 1. validate user input
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_info = serializer.validated_data
        # 2. Verify patent by first name and ccc_number
        ccc_number = verification_info.get('ccc_number')
        patient = self.find_remote_patient(ccc_number)
        if patient['f_name'] != verification_info.get("first_name"):
            raise VerificationException()
        patient_ob = self.get_or_create_patient(patient)
        # 3. Make sure there is no other account for that patient
        if patient_ob.user:
            raise VerificationException(detail="Account already exist for that patient")
        # 4. request verification
        verification = AccountVerification.objects.create(
            user=request.user,
            extra_value=patient_ob.patient_number
        )
        # TODO implement an sms send otp
        return Response({
            "message": f"Success!Check your number {request.user.profile.phone_number} messages for "
                       f"verification code within the next it expires in the next 5 minutes.",
            "verification_url": reverse(
                viewname='users:user-verify',
                request=request
            ),
        });

    def get_or_create_patient(self, remote_patient):
        try:
            patient = Patient.objects.get(patient_number=remote_patient.get('clinic_number'))
        except Patient.DoesNotExist:
            patient = Patient.objects.create(
                patient_number=remote_patient.get('clinic_number'),
                first_name=remote_patient.get('f_name'),
                last_name=remote_patient.get('m_name'),
                sur_name=remote_patient.get('l_name'),
                national_id=remote_patient.get('national_id'),
                date_of_birth=remote_patient.get('dob'),
                phone_number=remote_patient.get('phone_no')
            )
        return patient

    def find_remote_patient(self, upi):
        patients = search_patient(upi)
        return patients

    @action(
        methods=['get'], url_name='request-verification', url_path='verify-request', detail=False,
        permission_classes=[permissions.IsAuthenticated, custom_permissions.IsPatient,
                            custom_permissions.HasNoRelatedUserType])
    def request_verification(self, request, *args, **kwargs):
        account = request.GET.get("account")
        # validate query strong
        patient = self.is_valid(account)
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
            'message': f"Check your email {obscure_email(patient.email)} or "
                       f"phone number {obscure_number(str(patient.phone_number))} for verification "
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
        try:
            verification = AccountVerification.objects.get(
                code=code,
                user=request.user,
                is_verified=False,
                expiry_time__gt=timezone.now()
            )
            patient = Patient.objects.get(patient_number=verification.extra_value)
            patient.user = request.user
            patient.save()
            verification.is_verified = True
            verification.save()
            return Response(data={"detail": "Account verification successful"}, status=status.HTTP_200_OK)
        except AccountVerification.DoesNotExist:
            return Response(data={"detail": "Invalid or expired code!."}, status=status.HTTP_403_FORBIDDEN)
        except Patient.DoesNotExist:
            return Response(data={'detail': "Patient Not Found"}, status=status.HTTP_403_FORBIDDEN)

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
