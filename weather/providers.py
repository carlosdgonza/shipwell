import json

from django.conf import settings

# A dict where each filter is related with the proper endpoint to make consults.
sources = {
    'accuweather': '/accuweather?latitude={}&longitude={}',
    'noaa': '/noaa?latlon={},{}',
    'weather.com': '/weatherdotcom'
}


class Noaa:
    @staticmethod
    async def get_current_temp(lat, lon, source, session):
        # info = await requests.get(host+sources.get(source).format(lat, lon))
        async with session.get(settings.PROVIDERS_HOST + sources.get(source).format(lat, lon), retry_attempts=3) as response:
            info = await response.read()
            info = json.loads(info)
            info = info['today']['current']
            return {'F': info['fahrenheit'], 'C': info['celsius']}


class WeatherDotCom:
    @staticmethod
    async def get_current_temp(lat, lon, source, session):
        data = {"lat": lat, "lon": lon}
        async with session.post(settings.PROVIDERS_HOST + sources.get(source).format(lat, lon), json=data, retry_attempts=3) as response:
            info = await response.read()
            info = json.loads(info)
            info = info['query']['results']['channel']
            return {info['units']['temperature']: info['condition']['temp']}
        # info = await requests.post(host+sources.get(source), json=data)


class Accuweather:
    @staticmethod
    async def get_current_temp(lat, lon, source, session):
        async with session.get(settings.PROVIDERS_HOST+sources.get(source).format(lat, lon), retry_attempts=3) as response:
            info = await response.read()
            info = json.loads(info)
            info = info['simpleforecast']['forecastday'][0]['current']
            return {'F': info['fahrenheit'], 'C': info['celsius']}
