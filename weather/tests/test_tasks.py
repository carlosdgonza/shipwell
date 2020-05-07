from weather.tasks import calculate_avg_temperature

example_temperatures_1 = {'F': 80, 'C': 10}
example_temperatures_2 = {'F': 60, 'C': 30}
example_temperatures_3 = {'F': 40}


def test_calculate_avg_temperature():
    response = calculate_avg_temperature([example_temperatures_1, example_temperatures_2, example_temperatures_3])
    assert response['C'] == 20
    assert response['F'] == 60

