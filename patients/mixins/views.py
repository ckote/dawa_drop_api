from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from awards.serializers import PatientProgramEnrollmentSerializer, RedemptionSerializer
from core import permisions as custom_permissions
from patients.models import Patient


class LoyaltyPointsMixin:
    @action(
        permission_classes=[
            permissions.IsAuthenticated,
            custom_permissions.IsPatient,
            custom_permissions.HasRelatedUserType
        ],
        methods=['get'],
        url_path='my-points',
        url_name='points',
        detail=False
    )
    def my_points(self, request, *args, **kwargs):
        patient = request.user.patient
        data = {
            'total': patient.total_points,
            'total_redeemed_points': patient.total_redemption_points,
            'redeem_count': patient.redemptions.all().count(),
            'redeemable_points': patient.points_balance,
            'current_program_enrolment': PatientProgramEnrollmentSerializer(
                instance=patient.current_program_enrollment,
                context={'request': request}
            ).data if patient.current_program_enrollment is not None else None,
            'redeem_list': RedemptionSerializer(
                instance=patient.redemptions.all(),
                many=True,
                context={'request': request}
            ).data
        }
        return Response(data)

    @action(
        permission_classes=[
            permissions.IsAuthenticated,
            custom_permissions.IsPatient,
            custom_permissions.HasRelatedUserType
        ],
        methods=['get'],
        url_path='points-history',
        url_name='points-history',
        detail=False
    )
    def points_history(self, request, *args, **kwargs):
        from orders.models import DeliveryFeedBack
        from patients.serializers import PointsHistorySerializer

        feed_back = DeliveryFeedBack.objects.filter(delivery__order__appointment__patient__user=request.user)
        queryset = self.filter_queryset(feed_back)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PointsHistorySerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = PointsHistorySerializer(queryset, many=True)

        return Response(serializer.data)

    @action(
        permission_classes=[
            permissions.IsAuthenticated,
            custom_permissions.IsPatient,
            custom_permissions.HasRelatedUserType
        ],
        methods=['post'],
        url_path='redeem-points',
        url_name='redeem-points',
        detail=True,
        serializer_class=RedemptionSerializer
    )
    def redeem(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, id=kwargs['pk'], user=request.user)
        serializer = RedemptionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # TODO CHECK IF MAX REDEMPTION REACHED IN EITHER SERIALIZER validator or here
        points_redeemed = serializer.validated_data.get("reward").point_value
        instance = serializer.save(patient=patient, points_redeemed=points_redeemed)
        data = {
            'total': patient.total_points,
            'total_redeemed_points': patient.total_redemption_points,
            'redeem_count': patient.redemptions.all().count(),
            'redeemable_points': patient.points_balance,
            'program_enrolments': PatientProgramEnrollmentSerializer(
                instance=patient.enrollments,
                many=True,
                context={'request': request}
            ).data,
            'current_program_enrolment': PatientProgramEnrollmentSerializer(
                instance=patient.current_program_enrollment,
                context={'request': request}
            ).data if patient.current_program_enrollment is not None else None,
            'redemption': RedemptionSerializer(instance=instance, context={'request': request}).data
        }
        return Response(data)
