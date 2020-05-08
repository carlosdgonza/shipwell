# weather-api
Example API to get current temperature from different providers and calculate the average temperature.

## Setup 

### For Windows
```bash
python -m venv <venv_name>
path_to_venv\venv_name\Scripts\activate
(venv)pip install -r requirements.txt
```

## Running the application
```bash
(venv)python manage.py runserver
```

## Routes

Host:  http://127.0.0.1:8000/

### weather
GET /weather/?latitude=55&longitude=33&filters=noaa,weather.com

## Tests
```bash
(env)pytest
```