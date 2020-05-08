import asyncio
import aiohttp

from rest_framework import viewsets
from rest_framework.response import Response
from .tasks import get_temperature
from .serializers import CoordinatesSerializer
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

        # Checks if latitude and longitude are valid
        coordinates = CoordinatesSerializer(data={'latitude': latitude, 'longitude': longitude})
        coordinates.is_valid(raise_exception=True)

        # Checks that all required params were given
        if not filters:
            return Response({'filters': ['This field may not be null.']}, status=400)

        filters = map(str.strip, filters.split(','))
        # If some provider is not valid an exception will be caught.
        try:
            values = asyncio.run(get_temperature(latitude, longitude, filters))
        except AttributeError as e:
            return Response({'filters': ['Some providers given are not valid.']}, status=400)
        except aiohttp.client.ClientError as e:
            return Response({'filters': ['At this moment we are not being able to reach al the providers.']}, status=409)
        response['avg temperature']['current'] = values
        return JsonResponse(response)
