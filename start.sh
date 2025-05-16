#!/bin/bash

# Установка зависимостей Python
pip install -r requirements.txt

# Создание папок, если их нет
mkdir -p uploads
mkdir -p static/sample_data

# Генерация примера данных
python -c "exec(open('utils/generate_sample_data.py').read())"

# Запуск приложения с Gunicorn
gunicorn app:app --bind=0.0.0.0:3000 --workers=1 --threads=2