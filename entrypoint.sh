#!/bin/sh

# Ожидаем доступность БД
echo "Waiting for PostgreSQL to start..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

# Создаем миграции для моделей
echo "Making migrations..."
python manage.py makemigrations

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate

# Загружаем начальные данные, если есть
# echo "Loading initial data..."
# python manage.py load_initial_data

# Запускаем основную команду
echo "Starting server..."
exec "$@"