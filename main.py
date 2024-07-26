import sqlite3
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from model import AutocompleteRequest, CityRequest
from service import autocomplete_city, get_coordinates, get_weather

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DB_FILE = "weather_fastapi.db"
USER_ID_COOKIE = "user_id"

# CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Set-Cookie", "Cookie"],
)


@app.on_event("startup")
def startup():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY,
                city TEXT NOT NULL,
                user_id TEXT NOT NULL,
                search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user_id = request.cookies.get(USER_ID_COOKIE)
    if not user_id:
        user_id = str(uuid.uuid4())

    response = templates.TemplateResponse("index.html", {"request": request})
    response.set_cookie(USER_ID_COOKIE, user_id)
    return response


@app.post("/weather")
async def weather(city_request: CityRequest, request: Request):
    user_id = request.cookies.get(USER_ID_COOKIE)

    lat, lon = get_coordinates(city_request.city)
    if lat is not None and lon is not None:
        weather_data = get_weather(lat, lon)
        if weather_data:
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute("INSERT INTO search_history "
                             "(city, user_id) VALUES (?, ?)",
                             (city_request.city, user_id))
            return weather_data
    raise HTTPException(status_code=404,
                        detail="Город не найден или данные о погоде недоступны")


@app.post("/autocomplete")
async def autocomplete(autocomplete_request: AutocompleteRequest):
    return autocomplete_city(autocomplete_request.query)


@app.get("/history")
async def get_history():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT city, COUNT(city) "
                              "as count FROM search_history "
                              "GROUP BY city ORDER BY count DESC")
        return cursor.fetchall()


@app.get("/user_history")
async def get_user_history(request: Request):
    user_id = request.cookies.get(USER_ID_COOKIE)
    if not user_id:
        raise HTTPException(status_code=400, detail="Пользователь не идентифицирован")

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT city, COUNT(city) "
                              "as count FROM search_history "
                              "WHERE user_id = ? GROUP BY city "
                              "ORDER BY count DESC", (user_id,))
        return cursor.fetchall()
