from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import HIVLabTest, ARTRegimen, PatientHivMedication, Triad


class HIVLabTestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HIVLabTest
        fields = ('url', 'id', 'appointment', 'cd4_count', 'viral_load')
        extra_kwargs = {
            'url': {'view_name': 'medications:lab-test-detail'},
            'appointment': {'view_name': 'appointments:appointment-detail'},
        }


class ARTRegimenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ARTRegimen
        fields = ('url', 'id', 'regimen_line', 'regimen', 'created_at', 'updated_at')
        extra_kwargs = {
            'url': {'view_name': 'medications:regimen-detail'}
        }


class PatientHivMedicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PatientHivMedication
        fields = ('url', 'id', 'patient', 'regimen', 'doctor', 'is_current', 'created_at', 'updated_at')
        extra_kwargs = {
            'url': {'view_name': 'medications:patient-hiv-prescription-detail'},
            'patient': {'view_name': 'patients:patient-detail'},
            'regimen': {'view_name': 'medications:regimen-detail'},
            'doctor': {'view_name': 'doctors:doctor-detail'},
        }

    def to_representation(self, instance):
        _dict = super().to_representation(instance)
        regimen = _dict.pop("regimen")
        regimen_obje = {
            'regimen': ARTRegimenSerializer(
                instance=instance.regimen,
                context=self.context
            ).data if instance.regimen else None
        }
        _dict.update(regimen_obje)
        return _dict


class TriadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Triad
        fields = (
            'url',
            'appointment', 'weight', 'height',
            'temperature', 'heart_rate',
            'blood_pressure', 'created_at'
        )
        extra_kwargs = {
            'url': {'view_name': 'medications:triad-detail', 'read_only': True},
            'appointment': {'view_name': 'appointments:appointment-detail', 'read_only': True},
        }