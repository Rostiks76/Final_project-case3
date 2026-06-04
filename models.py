#Модуль с классами данных для приложения.
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Question:
    """
    Класс, представляющий вопрос викторины.
    
    Attributes:
        id: Уникальный идентификатор вопроса
        text: Текст вопроса
        options: Список вариантов ответа (4 штуки)
        correct_idx: Индекс правильного ответа (1-4)
    """
    id: int
    text: str
    options: List[str]
    correct_idx: int
    
    def is_correct(self, answer_idx: int) -> bool:
        """
        Проверяет, правильный ли ответ.
        
        Args:
            answer_idx: Индекс ответа пользователя (1-4)
            
        Returns:
            True, если ответ правильный, иначе False
        """
        return self.correct_idx == answer_idx


@dataclass
class LeaderboardEntry:
    """
    Класс, представляющий запись в таблице лидеров.
    
    Attributes:
        player_name: Имя игрока
        score: Набранный процент правильных ответов
        date_played: Дата и время игры
    """
    player_name: str
    score: int
    date_played: datetime