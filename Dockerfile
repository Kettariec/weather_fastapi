FROM python:3.11-slim
RUN pip install poetry
RUN poetry config virtualenvs.create false
WORKDIR /app
COPY . /app
RUN poetry install --no-dev
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]