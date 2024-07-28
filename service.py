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
           f"&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,"
           f"precipitation,weathercode&daily=temperature_2m_max,temperature_2m_min,"
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
        current_weathercode = current_weather.get("weathercode", "No data")

        weather_code_mapping = {
            0: "ясно",
            1: "в основном ясно",
            2: "частично облачно",
            3: "облачно",
            45: "туман",
            48: "изморозь",
            51: "легкий дождь",
            53: "умеренный дождь",
            55: "сильный дождь",
            56: "ледяной дождь",
            57: "сильный ледяной дождь",
            61: "легкий снег",
            63: "умеренный снег",
            65: "сильный снег",
            66: "легкий ледяной дождь",
            67: "сильный ледяной дождь",
            71: "легкий снегопад",
            73: "умеренный снегопад",
            75: "сильный снегопад",
            77: "град",
            80: "легкий ливень",
            81: "умеренный ливень",
            82: "сильный ливень",
            85: "легкий снегопад",
            86: "сильный снегопад",
            95: "грозы",
            96: "гроза с легким градом",
            99: "гроза с сильным градом",
        }

        current_weather_description = weather_code_mapping.get(current_weathercode, "Неизвестная погода")

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
            "current_weather_description": current_weather_description,
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
