from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
import requests

# Create your views here.


class PlacesSearchView(views.APIView):
    def get(self, request, *args, **kwargs):
        params = request.data
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
            'Authorization': '5b3ce3597851110001cf62489174bcdc8f554d299974dd0047a0e714',
            'Content-Type': 'application/json; charset=utf-8'
        }
        # params.update({'key': settings.MAPQUEST_CONSUMER_KEY, "q": request.GET.get('q'),'collection': 'adminArea,
        # poi,address,category,franchise,airport'}) response = requests.get(
        # url=settings.MAPQUEST_PLACES_API_ENDPOINT, params=params)
        params = {'text': request.GET.get('q')}
        response = requests.get(url=f'https://api.openrouteservice.org/geocode/autocomplete', params=params, headers=headers)
        if response.status_code == 200:
            pass
        else:
            pass
        PATH = settings.BASE_DIR / ".env"
        print(settings.MAPQUEST_CONSUMER_KEY, settings.MAPQUEST_CONSUMER_SECRETE, PATH.exists())
        return Response({"result": response.json()})
