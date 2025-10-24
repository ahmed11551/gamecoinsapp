"""
Веб-интерфейс для игр на Vercel
"""
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/game/<game_type>')
def game_page(game_type):
    """Страница игры"""
    if game_type == 'clicker':
        return render_template('clicker.html')
    elif game_type == 'reaction':
        return render_template('reaction.html')
    elif game_type == '2048':
        return render_template('2048.html')
    else:
        return "Игра не найдена", 404

@app.route('/api/game/submit', methods=['POST'])
def submit_game_result():
    """API для отправки результатов игры"""
    data = request.get_json()
    
    # Здесь должна быть логика обработки результатов
    # и отправка в Telegram бот
    
    return jsonify({
        "status": "success",
        "message": "Результат получен"
    })

if __name__ == '__main__':
    app.run(debug=True)
