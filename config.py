import os

# Путь к файлу базы данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "questions.db")

# Количество вариантов ответа на вопрос
NUM_OPTIONS = 4