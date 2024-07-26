import requests


def get_coordinates(city: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&language=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            return data["results"][0]["latitude"], data["results"][0]["longitude"]
    return None, None


def get_weather(lat: float, lon: float):
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&current_weather=true&hourly=temperature_2m,"
           f"relative_humidity_2m,wind_speed_10m")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        current_weather = data.get("current_weather", {})
        hourly = data.get("hourly", {})

        current_temp = current_weather.get("temperature", "No data")
        current_humidity = hourly.get("relative_humidity_2m", [])[0]
        current_wind_speed = hourly.get("wind_speed_10m", [])[0]

        return {
            "current_temperature": current_temp,
            "current_humidity": current_humidity,
            "current_wind_speed": current_wind_speed
        }
    return None


def autocomplete_city(query: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&language=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            return [result["name"] for result in data["results"]]
    return []
