FROM python:3.11-slim

# Не писать .pyc и сразу показывать логи
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала зависимости — так кеш быстрее
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом весь проект
COPY . .

# Запуск бота (polling)
CMD ["python", "-m", "app.main"]
