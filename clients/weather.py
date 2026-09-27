from clients.http import get_json
from clients.exceptions import NotFoundError


WEATHER_CODES = {
	"0": "Clear sky",
	"1": "Mainly clear",
	"2": "Partly cloudy",
	"3": "Overcast",
	"45": "Fog",
	"48": "Depositing rime fog",
	"51": "Light drizzle",
	"53": "Moderate drizzle",
	"55": "Dense drizzle",
	"56": "Light freezing drizzle",
	"57": "Dense freezing drizzle",
	"61": "Slight rain",
	"63": "Moderate rain",
	"65": "Heavy rain",
	"66": "Light freezing rain",
	"67": "Heavy freezing rain",
	"71": "Slight snowfall",
	"73": "Moderate snowfall",
	"75": "Heavy snowfall",
	"77": "Snow grains",
	"80": "Slight rain showers",
	"81": "Moderate rain showers",
	"82": "Violent rain showers",
	"85": "Slight snow showers",
	"86": "Heavy snow showers",
	"95": "Thunderstorm",
	"96": "Thunderstorm with slight hail",
	"97": "Heavy thunderstorm",
	"99": "Thunderstorm with heavy hail"
}

def get_coordinates(city: str) -> tuple[float,float]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name":city, "count":1}
    data = get_json(url=url, params=params)

    if not data.get("results"):
        raise NotFoundError(f"City {city} not found")

    results = data["results"][0]

    if "latitude" not in results:
        raise ValueError("Отсутствует поле latitude")

    if "longitude" not in results:
        raise ValueError("Отсутствует поле longitude")

    latitude = results["latitude"]
    longitude = results["longitude"]

    return (latitude, longitude)


def get_forecast(latitude: float,longitude: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":latitude, 
        "longitude":longitude,
        "current": "temperature_2m,weather_code"
        }
    data = get_json(url=url, params = params)

    if not data.get("current"):
        raise ValueError("Отсутствует поле current")

    if "temperature_2m" not in data["current"]:
        raise ValueError("Отсутствует поле temperature_2m")

    if "weather_code" not in data["current"]:
        raise ValueError("Отсутствует поле weather_code")

    description = WEATHER_CODES.get(str(data["current"]["weather_code"]),"unknown")
    temperature = data["current"]["temperature_2m"]

    return {
        "temp_c":temperature,
        "description":description
        }

def get_weather(city: str) -> dict:
    lat, lon = get_coordinates(city)
    return get_forecast(lat, lon)