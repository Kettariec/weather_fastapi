import sqlite3

import pytest
from fastapi.testclient import TestClient

from main import DB_FILE, app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                user_id TEXT NOT NULL,
                search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    yield


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "Погода в вашем городе" in response.text


def test_get_coordinates():
    from service import get_coordinates
    lat, lon = get_coordinates("Москва")
    assert lat is not None
    assert lon is not None


def test_get_weather():
    from service import get_weather
    lat, lon = 55.7558, 37.6173
    weather_data = get_weather(lat, lon)
    assert weather_data is not None
    assert "current_temperature" in weather_data


@pytest.mark.asyncio
async def test_weather():
    response = client.post("/weather", json={"city": "Москва", "user_id": "test_user"})
    assert response.status_code == 200
    weather_data = response.json()
    assert "current_temperature" in weather_data


@pytest.mark.asyncio
async def test_autocomplete():
    response = client.post("/autocomplete", json={"query": "Мос"})
    assert response.status_code == 200
    suggestions = response.json()
    assert "Москва" in suggestions


@pytest.mark.asyncio
async def test_get_history():
    response = client.get("/history")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)


@pytest.mark.asyncio
async def test_get_user_history():
    response = client.get("/user_history", cookies={"user_id": "test_user"})
    assert response.status_code == 200
    user_history = response.json()
    assert isinstance(user_history, list)
