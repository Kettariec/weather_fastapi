
<h2 align="center">Application Weather</h2>

Приложение для просмотра погоды.


<!-- USAGE EXAMPLES -->
## Usage

Перед запуском web-приложения установите виртуальное окружение Poetry и необходимые пакеты из файла pyproject.toml. Для запуска используйте команду "uvicorn main:app".


## Docker 
Создайте образ и контейнер Docker с помощью команды "docker-compose up --build".


## Структура проекта

templates/index.html - шаблон главной страницы.

.flake8 - файл конфигурации flake8.

.gitignore - файл Git.

.dockerignore<br>
Dockerfile<br>
docker-compose.yaml - файлы Docker.

main.py - точка входа приложения и роутеры, настроен CORS.

model.py - файл с моделями запроса и автозаполнения.

pyproject.toml<br>
poetry.lock - файлы Poetry.

service.py - функции приложения.

test_main.py - тесты, для запуска используйте команду "pytest".

weather_fastapi.db - база данных SQLite.

<!-- CONTACT -->
## Contact

kettariec@gmail.com

https://github.com/Kettariec/weather_fastapi

<p align="right">(<a href="#readme-top">back to top</a>)</p>