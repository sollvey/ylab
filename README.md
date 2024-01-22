Создаём виртуальную среду `python -m venv venv`\
Выбираем виртуальную среду `.\venv\Scripts\activate`\
Устанавливаем зависимости `pip install -r requirements.txt`\
Выполняем миграции `python migration.py`\
Запускаем веб-сервер `uvicorn main:app --host localhost --port 8000`