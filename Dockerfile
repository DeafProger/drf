# Используем базовый образ Python
FROM python:3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /coursework

# Копируем зависимости в контейнер
COPY ./requirements.txt /coursework/

# Устанавливаем зависимости
RUN pip install -r /coursework/requirements.txt

# Копируем код приложения в контейнер
COPY . .