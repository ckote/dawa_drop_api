from rest_framework import routers
from django.urls import path

app_name = 'medications'

from .views import (
    PatientHIVLabTestViewSet, PatientHivMedicationViewSet, ARTRegimenViewSet, TriadViewSet)

router = routers.DefaultRouter()
router.register(prefix=r'patient-tests', viewset=PatientHIVLabTestViewSet, basename='lab-test')
router.register(prefix=r'triads', viewset=TriadViewSet, basename='triad')
router.register(prefix=r'regimens', viewset=ARTRegimenViewSet, basename='regimen')
router.register(prefix=r'', viewset=PatientHivMedicationViewSet, basename='patient-hiv-prescription')

urlpatterns = router.urls
