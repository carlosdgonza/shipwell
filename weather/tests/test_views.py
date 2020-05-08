import asynctest
import aiohttp

both_temperature_response = {'F': 33, 'C': 44}
fahrenheit_response = {'F': 33}


def test_wrong_latitude(django_client):
    """Call to endpoint must fail when is passed a no numeric latitude."""
    latitude = 'not_valid'
    response = django_client.get('/weather/?latitude={}&longitude=33&filters=weather.com,noaa'.format(latitude))
    assert response.status_code == 400


def test_wrong_longitude(django_client):
    """Call to endpoint must fail when is passed a no numeric longitude."""
    longitude = 'not_valid'
    response = django_client.get('/weather/?latitude=44&longitude={}&filters=weather.com,noaa'.format(longitude))
    assert response.status_code == 400


def test_negative_latitude_longitude(django_client):
    """Call to endpoint must succeed when passing a negative values for latitude and/or longitude."""
    latitude = -40
    longitude = -30
    with asynctest.mock.patch('weather.providers.Noaa.get_current_temp', side_effect=[both_temperature_response]):
        response = django_client.get('/weather/?latitude={}&longitude={}&filters=noaa'.format(latitude, longitude))
        assert response.status_code == 200


def test_no_filters(django_client):
    """Call to endpoint must fail if no filter was passed as param."""
    response = django_client.get('/weather/?latitude=33&longitude=44')
    assert response.status_code == 400
    assert response.data == {'filters': ['This field may not be null.']}


def test_no_latitude(django_client):
    """Call to endpoint must fail if no latitude was passed as param."""
    response = django_client.get('/weather/?longitude=44&filters=weather.com,noaa')
    assert response.status_code == 400


def test_no_longitude(django_client):
    """Call to endpoint must fail if no longitude was passed as param."""
    response = django_client.get('/weather/?latitude=33&filters=weather.com,noaa')
    assert response.status_code == 400


def test_wrong_filters(django_client):
    """Call to endpoint must fail if any filter is not valid."""
    filters = 'not_valid'
    response = django_client.get('/weather/?latitude=44&longitude=33&filters={}'.format(filters))
    assert response.status_code == 400
    assert response.data == {'filters': ['Some providers given are not valid.']}


def test_single_filters(django_client):
    """Call to endpoint must succeed when passing all valid params and just one filter as source"""
    filters = 'noaa'
    with asynctest.mock.patch('weather.providers.Noaa.get_current_temp', side_effect=[both_temperature_response]):
        response = django_client.get('/weather/?latitude=44&longitude=33&filters={}'.format(filters))
        assert response.status_code == 200


def test_multiple_filters(django_client):
    """Call to endpoint must succeed when passing all valid params and multiple filters as sources"""
    with asynctest.mock.patch('weather.providers.Noaa.get_current_temp', side_effect=[both_temperature_response]):
        with asynctest.mock.patch('weather.providers.WeatherDotCom.get_current_temp', side_effect=[fahrenheit_response]):
            filters = 'noaa, weather.com'
            response = django_client.get('/weather/?latitude=44&longitude=33&filters={}'.format(filters))
            assert response.status_code == 200


def test_any_provider_connection_is_down(django_client):
    """Call to endpoint must throw a message that the service cannot provide the information at the moment."""
    with asynctest.mock.patch('weather.providers.Noaa.get_current_temp',
                              side_effect=aiohttp.client.ClientError):
        filters = 'noaa'
        response = django_client.get('/weather/?latitude=44&longitude=33&filters={}'.format(filters))
        assert response.status_code == 409
        assert response.data == {'filters': ['At this moment we are not being able to reach al the providers.']}


def test_greater_allowed_latitude(django_client):
    """Call to endpoint must fail and throw a message if an greater latitude than allowed is provided"""
    latitude = 91
    response = django_client.get('/weather/?latitude={}&longitude=180&filters=weather.com,noaa'.format(latitude))
    assert response.status_code == 400


def test_lower_allowed_latitude(django_client):
    """Call to endpoint must fail and throw a message if an lower latitude than allowed is provided"""
    latitude = -91
    response = django_client.get('/weather/?latitude={}&longitude=-180&filters=weather.com,noaa'.format(latitude))
    assert response.status_code == 400


def test_greater_allowed_longitude(django_client):
    """Call to endpoint must fail and throw a message if an greater longitude than allowed is provided"""
    latitude = 181
    response = django_client.get('/weather/?latitude=-90&longitude={}&filters=weather.com,noaa'.format(latitude))
    assert response.status_code == 400


def test_lower_allowed_longitude(django_client):
    """Call to endpoint must fail and throw a message if an lower longitude than allowed is provided"""
    latitude = -181
    response = django_client.get('/weather/?latitude=90&longitude={}&filters=weather.com,noaa'.format(latitude))
    assert response.status_code == 400
