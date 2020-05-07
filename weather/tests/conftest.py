import pytest
import asynctest
import weather

from django.test import Client

noaa_response = { "today": { "high": { "fahrenheit": "68", "celsius": "20" }, "low": { "fahrenheit": "50", "celsius": "10" },
             "current": { "fahrenheit": "55", "celsius": "12" } } }


@pytest.fixture(scope='module')
def django_client():
    c = Client()
    yield c


@pytest.fixture(scope='module')
def mock_noaa():
    return asynctest.patch('weather.providers.Noaa.get_current_temp',  side_effect=noaa_response)
    # return asynctest.CoroutineMock(weather.providers.Noaa.get_current_temp, side_effect=noaa_response)
