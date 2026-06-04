import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime

from config import DB_PATH, NUM_OPTIONS


def get_connection() -> sqlite3.Connection:
    # Возвращает соединение с базой данных.
    return sqlite3.connect(DB_PATH)


def init_database() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Таблица вопросов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                option_1 TEXT NOT NULL,
                option_2 TEXT NOT NULL,
                option_3 TEXT NOT NULL,
                option_4 TEXT NOT NULL,
                correct_idx INTEGER NOT NULL CHECK(correct_idx BETWEEN 1 AND 4)
            )
        """)
        
        # Таблица лидеров
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date_played TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Проверяем, есть ли вопросы
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        
        if count == 0:
            _seed_questions(cursor)
        
        conn.commit()


def _seed_questions(cursor: sqlite3.Cursor) -> None:
    questions = [
        ("Столица Франции?", "Берлин", "Лондон", "Париж", "Мадрид", 3),
        ("Сколько планет в Солнечной системе?", "7", "8", "9", "10", 2),
        ("Кто написал 'Войну и мир'?", "Достоевский", "Толстой", "Чехов", "Пушкин", 2),
        ("Python - это...", "Змея", "Язык программирования", "И то, и другое", "Ни то, ни другое", 3),
        ("Что означает аббревиатура ООП?", "Объектно-ориентированное программирование", "Очень опасный путь", "Основной оператор печати", "Организация охраны природы", 1),
        ("Git - это...", "Язык программирования", "Система контроля версий", "База данных", "Операционная система", 2),
    ]
    
    for q in questions:
        cursor.execute("""
            INSERT INTO questions (text, option_1, option_2, option_3, option_4, correct_idx)
            VALUES (?, ?, ?, ?, ?, ?)
        """, q)


def get_all_questions() -> List[Dict[str, Any]]:
   
    # Возвращает все вопросы из базы данных.
    
    # Returns:
        # Список словарей с ключами: id, text, options, correct_idx

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        rows = cursor.fetchall()
    
    questions = []
    for row in rows:
        questions.append({
            "id": row[0],
            "text": row[1],
            "options": [row[2], row[3], row[4], row[5]],
            "correct_idx": row[6]
        })
    
    return questions


def save_score(name: str, score: int) -> None:
    # Сохраняет результат игрока в таблицу лидеров.
    
   # Args:
       # name: Имя игрока
       # score: Набранный процент правильных ответов (0-100)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leaderboard (player_name, score, date_played)
            VALUES (?, ?, ?)
        """, (name, score, datetime.now()))
        conn.commit()


def get_leaderboard(limit: int = 10) -> List[Dict[str, Any]]:

    # Возвращает таблицу лидеров (сортировка по убыванию баллов).
    
    # Args:
        # limit: Максимальное количество записей
        
    # Returns:
        # Список словарей с ключами: player_name, score, date_played

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT player_name, score, date_played
            FROM leaderboard
            ORDER BY score DESC, date_played ASC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
    
    return [
        {"player_name": row[0], "score": row[1], "date_played": row[2]}
        for row in rows
    ]