from django.urls import path
from . import views
app_name = 'services'
urlpatterns = [
    path("places/", views.PlacesSearchView.as_view(), name='places'),
]