from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import (
    UserSerializer

)
from users import mixin as mixins


class UserViewSet(
    viewsets.ModelViewSet,
    mixins.DoctorsMixin,
    mixins.PatientsMixin,
    mixins.AgentsMixin,
    mixins.AuthMixin,
    mixins.ProfileMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]

    @action(
        methods=['get'],
        detail=False,
        authentication_classes=[TokenAuthentication],
        permission_classes=[
            IsAuthenticated
        ],
        description="Get user by token",
        url_path='get-user-by-token'
    )
    def get_user_by_token(self, request, *args, **kwargs):
        user = request.user
        return Response(self.get_serializer(instance=user).data)
