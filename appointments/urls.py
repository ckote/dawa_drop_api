from rest_framework import routers

from .views import AppointMentTypeViewSet, AppointMentViewSet

app_name = 'appointments'
router = routers.DefaultRouter()

router.register(viewset=AppointMentTypeViewSet, prefix='types', basename='type')
router.register(prefix=r'', viewset=AppointMentViewSet, basename='appointment')

urlpatterns = router.urls
