Изменяем значения переменных окружения на свои в `.env`\
Создаём виртуальную среду `python -m venv venv`\
Активируем виртуальную среду `.\venv\Scripts\activate`\
Устанавливаем зависимости `pip install -r requirements.txt`\
Выполняем миграции `python migration.py`\
Запускаем веб-сервер `uvicorn main:app --host localhost --port 8000`