from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
from database import init_database, get_all_questions, save_score, get_leaderboard
from models import Question



app = Flask(__name__)
app.secret_key = 'secret-key-for-viktorina'  # Для сессий
app.jinja_env.globals.update(enumerate=enumerate)
init_database()


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/start', methods=['GET', 'POST'])
def start_quiz():
    """Старт викторины — запрос имени"""
    if request.method == 'POST':
        name = request.form.get('player_name', '').strip()
        if name:
            session['player_name'] = name
            session['question_index'] = 0
            session['correct_count'] = 0
            
            # Загружаем и перемешиваем вопросы
            questions_data = get_all_questions()
            questions = [
                {
                    'id': q['id'],
                    'text': q['text'],
                    'options': q['options'],
                    'correct_idx': q['correct_idx']
                }
                for q in questions_data
            ]
            random.shuffle(questions)
            session['questions'] = questions
            session['total'] = len(questions)
            
            return redirect(url_for('quiz'))
    
    return render_template('start.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = session.get('questions', [])
    index = session.get('question_index', 0)
    total = session.get('total', 0)
    
    if index >= len(questions):
        return redirect(url_for('result'))
    
    current_question = questions[index]
    
    if request.method == 'POST':
        answer = int(request.form.get('answer', 0))
        is_correct = (answer == current_question['correct_idx'])
        correct_answer_text = current_question['options'][current_question['correct_idx'] - 1]
        
        if is_correct:
            session['correct_count'] = session.get('correct_count', 0) + 1
        
        session['question_index'] = index + 1
        
        # Возвращаем JSON для AJAX-запроса
        from flask import jsonify
        return jsonify({
            'correct': is_correct,
            'correct_answer': correct_answer_text,
            'next_url': url_for('quiz') if session['question_index'] < total else url_for('result')
        })
    
    return render_template('quiz.html', 
                          question=current_question, 
                          current=index + 1, 
                          total=total)


@app.route('/result')
def result():
    """Результат викторины"""
    correct = session.get('correct_count', 0)
    total = session.get('total', 1)
    score = round((correct / total) * 100)
    
    player_name = session.get('player_name', 'Неизвестный')
    
    # Сохраняем результат в БД
    save_score(player_name, score)
    
    return render_template('result.html', 
                          name=player_name, 
                          correct=correct, 
                          total=total, 
                          score=score)


@app.route('/leaderboard')
def leaderboard():
    """Таблица лидеров"""
    entries = get_leaderboard(limit=10)
    return render_template('leaderboard.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)