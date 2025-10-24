"""
Игра Тест на реакцию
"""
import time
import random
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ReactionTestResult:
    attempts: List[float]  # времена реакции в мс
    average_reaction: float
    best_reaction: float
    worst_reaction: float
    score: float
    is_valid: bool


class ReactionTestGame:
    def __init__(self):
        self.num_attempts = 10
        self.min_reaction_time = 100  # мс
        self.max_reaction_time = 2000  # мс
        self.min_delay = 1000  # мс
        self.max_delay = 5000  # мс
        
    def start_game(self) -> Dict[str, Any]:
        """Начать игру"""
        return {
            "game_type": "reaction",
            "attempts": self.num_attempts,
            "instructions": f"Нажмите кнопку как можно быстрее, когда она станет зеленой! ({self.num_attempts} попыток)",
            "start_time": time.time()
        }
    
    def process_results(self, results_data: Dict[str, Any]) -> ReactionTestResult:
        """Обработать результаты теста"""
        attempts = results_data.get("attempts", [])
        start_time = results_data.get("start_time", time.time())
        
        if len(attempts) != self.num_attempts:
            return ReactionTestResult(
                attempts=attempts,
                average_reaction=0,
                best_reaction=0,
                worst_reaction=0,
                score=0,
                is_valid=False
            )
        
        # Проверяем валидность времен реакции
        valid_attempts = []
        for attempt in attempts:
            if self.min_reaction_time <= attempt <= self.max_reaction_time:
                valid_attempts.append(attempt)
        
        if len(valid_attempts) < self.num_attempts * 0.8:  # минимум 80% валидных попыток
            return ReactionTestResult(
                attempts=attempts,
                average_reaction=0,
                best_reaction=0,
                worst_reaction=0,
                score=0,
                is_valid=False
            )
        
        # Рассчитываем статистику
        average_reaction = sum(valid_attempts) / len(valid_attempts)
        best_reaction = min(valid_attempts)
        worst_reaction = max(valid_attempts)
        
        # Рассчитываем очки (чем быстрее реакция, тем больше очков)
        score = max(0, 1000 - average_reaction) * len(valid_attempts) / self.num_attempts
        
        return ReactionTestResult(
            attempts=attempts,
            average_reaction=average_reaction,
            best_reaction=best_reaction,
            worst_reaction=worst_reaction,
            score=score,
            is_valid=True
        )
    
    def generate_webview_html(self) -> str:
        """Генерировать HTML для WebView"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Тест на реакцию</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .game-container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 400px;
            margin: 0 auto;
        }
        
        .title {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
        
        .attempt-counter {
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 20px;
        }
        
        .reaction-button {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            border: none;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            margin: 20px auto;
            display: block;
        }
        
        .reaction-button.waiting {
            background: #e74c3c;
            color: white;
        }
        
        .reaction-button.waiting:hover {
            background: #c0392b;
        }
        
        .reaction-button.ready {
            background: #27ae60;
            color: white;
            animation: pulse 0.5s infinite;
        }
        
        .reaction-button.too-early {
            background: #f39c12;
            color: white;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .stat-label {
            font-size: 12px;
            color: #7f8c8d;
        }
        
        .start-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
            margin: 20px 0;
        }
        
        .start-btn:hover {
            background: #2980b9;
        }
        
        .start-btn:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
        }
        
        .game-over {
            display: none;
        }
        
        .final-score {
            font-size: 32px;
            color: #e74c3c;
            margin: 20px 0;
        }
        
        .attempts-list {
            text-align: left;
            margin: 20px 0;
        }
        
        .attempt-item {
            padding: 5px 0;
            border-bottom: 1px solid #ecf0f1;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="title">⚡ Тест на реакцию</div>
        
        <div id="game-area">
            <div class="attempt-counter" id="attemptCounter">Попытка 1 из 10</div>
            
            <button class="reaction-button waiting" id="reactionBtn">Нажмите когда кнопка станет зеленой</button>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="averageReaction">0</div>
                    <div class="stat-label">Среднее (мс)</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="bestReaction">0</div>
                    <div class="stat-label">Лучшее (мс)</div>
                </div>
            </div>
            
            <button class="start-btn" id="startBtn">Начать тест</button>
        </div>
        
        <div id="game-over" class="game-over">
            <div class="final-score" id="finalScore">0</div>
            <div>Средняя реакция: <span id="finalAverage">0</span> мс</div>
            <div>Лучшая реакция: <span id="finalBest">0</span> мс</div>
            
            <div class="attempts-list" id="attemptsList"></div>
            
            <button class="start-btn" onclick="location.reload()">Пройти снова</button>
        </div>
    </div>

    <script>
        let gameStarted = false;
        let gameEnded = false;
        let currentAttempt = 0;
        let attempts = [];
        let reactionStartTime = 0;
        let waitingForClick = false;
        let timeoutId = null;
        
        const reactionBtn = document.getElementById('reactionBtn');
        const startBtn = document.getElementById('startBtn');
        const attemptCounter = document.getElementById('attemptCounter');
        const averageReaction = document.getElementById('averageReaction');
        const bestReaction = document.getElementById('bestReaction');
        const gameArea = document.getElementById('game-area');
        const gameOver = document.getElementById('game-over');
        const finalScore = document.getElementById('finalScore');
        const finalAverage = document.getElementById('finalAverage');
        const finalBest = document.getElementById('finalBest');
        const attemptsList = document.getElementById('attemptsList');
        
        function startGame() {
            gameStarted = true;
            gameEnded = false;
            currentAttempt = 0;
            attempts = [];
            startBtn.disabled = true;
            
            startNextAttempt();
        }
        
        function startNextAttempt() {
            if (currentAttempt >= 10) {
                endGame();
                return;
            }
            
            currentAttempt++;
            attemptCounter.textContent = `Попытка ${currentAttempt} из 10`;
            
            // Случайная задержка перед появлением зеленой кнопки
            const delay = Math.random() * 4000 + 1000; // 1-5 секунд
            
            reactionBtn.className = 'reaction-button waiting';
            reactionBtn.textContent = 'Ждите...';
            reactionBtn.disabled = true;
            waitingForClick = false;
            
            timeoutId = setTimeout(() => {
                reactionBtn.className = 'reaction-button ready';
                reactionBtn.textContent = 'КЛИКАЙ!';
                reactionBtn.disabled = false;
                reactionStartTime = Date.now();
                waitingForClick = true;
                
                // Таймаут на случай если пользователь не кликнет
                setTimeout(() => {
                    if (waitingForClick) {
                        handleClick(0); // 0 означает что не успел
                    }
                }, 2000);
                
            }, delay);
        }
        
        function handleClick(reactionTime = null) {
            if (!waitingForClick) {
                // Клик слишком рано
                reactionBtn.className = 'reaction-button too-early';
                reactionBtn.textContent = 'Слишком рано!';
                attempts.push(0);
                
                setTimeout(() => {
                    startNextAttempt();
                }, 1000);
                return;
            }
            
            if (reactionTime === null) {
                reactionTime = Date.now() - reactionStartTime;
            }
            
            attempts.push(reactionTime);
            waitingForClick = false;
            
            // Показываем результат попытки
            reactionBtn.textContent = `${reactionTime} мс`;
            
            setTimeout(() => {
                startNextAttempt();
            }, 1000);
            
            updateStats();
        }
        
        function updateStats() {
            const validAttempts = attempts.filter(a => a > 0);
            
            if (validAttempts.length > 0) {
                const average = validAttempts.reduce((a, b) => a + b, 0) / validAttempts.length;
                const best = Math.min(...validAttempts);
                
                averageReaction.textContent = Math.round(average);
                bestReaction.textContent = Math.round(best);
            }
        }
        
        function endGame() {
            gameEnded = true;
            
            const validAttempts = attempts.filter(a => a > 0);
            const average = validAttempts.reduce((a, b) => a + b, 0) / validAttempts.length;
            const best = Math.min(...validAttempts);
            const score = Math.max(0, 1000 - average) * validAttempts.length / 10;
            
            // Показываем результаты
            finalAverage.textContent = Math.round(average);
            finalBest.textContent = Math.round(best);
            finalScore.textContent = Math.round(score);
            
            // Показываем список попыток
            attemptsList.innerHTML = '';
            attempts.forEach((attempt, index) => {
                const div = document.createElement('div');
                div.className = 'attempt-item';
                div.textContent = `Попытка ${index + 1}: ${attempt > 0 ? attempt + ' мс' : 'Слишком рано'}`;
                attemptsList.appendChild(div);
            });
            
            gameArea.style.display = 'none';
            gameOver.style.display = 'block';
            
            // Отправляем результаты в Telegram
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.sendData(JSON.stringify({
                    attempts: attempts,
                    start_time: Date.now() / 1000,
                    average_reaction: average,
                    best_reaction: best,
                    score: score
                }));
            }
        }
        
        // Обработчики событий
        startBtn.addEventListener('click', startGame);
        reactionBtn.addEventListener('click', () => handleClick());
        
        // Инициализация Telegram WebApp
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
        }
    </script>
</body>
</html>
        """
