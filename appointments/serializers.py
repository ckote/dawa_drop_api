from rest_framework import serializers

from .models import AppointMentType, AppointMent


class AppointMentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppointMentType
        fields = ('url', 'type', 'description', 'created_at')
        extra_kwargs = {
            'url': {'view_name': 'core:appointment-types-detail'}
        }


class AppointMentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppointMent
        fields = (
            'url', 'id', 'patient', 'type', 'doctor', 'next_appointment_date',
            'created_at', 'updated_at'
        )
        extra_kwargs = {
            'url': {'view_name': 'patients:appointment-detail'},
            'patient': {'view_name': 'patients:patient-detail'},
            'type': {'view_name': 'core:appointment-types-detail'},
            'doctor': {'view_name': 'doctors:doctor-detail'},
        }

    def to_representation(self, instance):
        _dict = super().to_representation(instance)
        from users.serializers import PublicProfileSerializer
        _dict.update({
            'doctor': PublicProfileSerializer(instance=instance.doctor.user.profile, context=self.context).data,
            'type': AppointMentTypeSerializer(instance=instance.type, context=self.context).data
        })
        return _dict
