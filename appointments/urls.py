from rest_framework import routers

from .views import AppointMentTypeViewSet, AppointMentViewSet

router = routers.DefaultRouter()

router.register(viewset=AppointMentTypeViewSet, prefix='types', basename='appointment-types')
router.register(prefix=r'', viewset=AppointMentViewSet, basename='appointment')

urlpatterns = router.urls
