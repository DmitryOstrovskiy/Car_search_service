# Базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем только файл с зависимостями в рабочую директорию
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы проекта
COPY . /app/

# Копируем файл entrypoint.sh и делаем его исполняемым
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Указываем порт, который будет слушать приложение
EXPOSE 8000

# Запускаем скрипт входа, как точку входа для контейнера
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# Задаем команду по умолчанию, которая будет выполнена после скрипта entrypoint.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
