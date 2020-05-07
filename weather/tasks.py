import asyncio
import aiohttp

from aiohttp_retry import RetryClient
from .providers import Accuweather, Noaa, WeatherDotCom

# A dict to correlate each filter with a provider class
providers = {'accuweather': Accuweather,
             'noaa': Noaa,
             'weather.com': WeatherDotCom
             }


async def get_temperature(lat, lon, filters):
    """
    A coroutine that would distribute tasks to get the necessary information about weather from
    the different providers.
    :param lat: str. atitude to consult the temperature
    :param lon: str. Longitude to consult the temperature
    :param filters: list - str. A list of external provider where the temperature info will be gotten
    :return: Calculated average temperature from the different providers.
    """
    async with RetryClient() as session:
        tasks = []
        try:
            for source in filters:
                task = asyncio.ensure_future(providers.get(source).get_current_temp(lat, lon, source, session))
                tasks.append(task)  # create list of tasks
            response = await asyncio.gather(*tasks)  # gather task responses
            avg_temp = calculate_avg_temperature(response)
        except (AttributeError, aiohttp.client.ClientError) as e:
            raise e
        return avg_temp


def calculate_avg_temperature(data):
    """
    Method to calculate the average temperature (Celsius and Fahrenheit) from a set of them.
    :param data: list - dict. List of dicts where each element has the temperature in Fahrenheit and Celsius.
    :return: float. Average temperature in Celsius and Fahrenheit.
    """
    avg_temp = dict()
    for elem in data:
        for key, value in elem.items():
            avg_temp[key] = (avg_temp.get(key, []) + [float(value)])
    for key, _ in avg_temp.items():
        avg_temp[key] = sum(avg_temp[key])/len(avg_temp[key])
    return avg_temp
