import asyncio
import aiohttp

from rest_framework import viewsets
from rest_framework.response import Response
from .tasks import get_temperature
from django.http import JsonResponse


class WeatherViewSet(viewsets.ViewSet):
    """
    View that shows the average temperature for a specific latitude and longitude extracted from different sources.
    """
    def list(self, request):
        response = {'avg temperature': dict()}
        query_params = self.request.query_params
        latitude = query_params.get('latitude', None)
        longitude = query_params.get('longitude', None)
        filters = query_params.get('filters', None)

        # Checks that all required params were given
        if not latitude or not longitude:
            return Response("Latitude and longitude params must be provided.", status=400)
        if not filters:
            return Response("At least one filter must be provided to validate into a provider.", status=400)

        # Checks if the latitude and longitude given are numbers
        try:
            lat, lon = float(latitude), float(longitude)
        except ValueError as e:
            return Response("Latitude and longitude must be numbers.", status=400)
        filters = map(str.strip, filters.split(','))
        # If some provider is not valid an exception will be caught.
        try:
            values = asyncio.run(get_temperature(latitude, longitude, filters))
        except AttributeError as e:
            return Response("Some providers given are not valid.", status=400)
        except aiohttp.client.ClientError as e:
            return Response("At this moment we are not being able to reach al the providers.", status=409)
        response['avg temperature']['current'] = values
        return JsonResponse(response)
