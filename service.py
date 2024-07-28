import requests

from datetime import datetime
from babel.dates import format_datetime


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
           f"&current_weather=true&hourly=temperature_2m,relative_humidity_2m,"
           f"wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,"
           f"precipitation_sum,relative_humidity_2m_max,relative_humidity_2m_min,"
           f"wind_speed_10m_max,wind_speed_10m_min")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        current_weather = data.get("current_weather", {})
        hourly = data.get("hourly", {})
        daily = data.get("daily", {})

        current_temp = current_weather.get("temperature", "No data")
        current_humidity = hourly.get("relative_humidity_2m", [])[0]
        current_wind_speed = hourly.get("wind_speed_10m", [])[0]

        weekly_forecast = []
        for i in range(len(daily.get("time", []))):
            date_str = daily["time"][i]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day_of_week = format_datetime(date_obj, "EEEE", locale="ru")
            forecast = {
                "date": date_str,
                "day_of_week": day_of_week,
                "max_temp": daily["temperature_2m_max"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
                "max_humidity": daily["relative_humidity_2m_max"][i],
                "min_humidity": daily["relative_humidity_2m_min"][i],
                "max_wind_speed": daily["wind_speed_10m_max"][i],
                "min_wind_speed": daily["wind_speed_10m_min"][i]
            }
            weekly_forecast.append(forecast)

        return {
            "current_temperature": current_temp,
            "current_humidity": current_humidity,
            "current_wind_speed": current_wind_speed,
            "weekly_forecast": weekly_forecast
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
