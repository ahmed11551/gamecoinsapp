"""
Игра Кликер - тест на скорость кликов
"""
import time
import random
from typing import Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class ClickerGameResult:
    clicks: int
    time_seconds: float
    cps: float  # clicks per second
    score: float
    is_valid: bool


class ClickerGame:
    def __init__(self):
        self.game_duration = 10  # секунд
        self.min_cps = 0.5  # минимальный CPS для валидации
        self.max_cps = 20.0  # максимальный CPS для валидации
        
    def start_game(self) -> Dict[str, Any]:
        """Начать игру"""
        return {
            "game_type": "clicker",
            "duration": self.game_duration,
            "instructions": f"Кликайте как можно быстрее в течение {self.game_duration} секунд!",
            "start_time": time.time()
        }
    
    def process_clicks(self, clicks_data: Dict[str, Any]) -> ClickerGameResult:
        """Обработать результаты кликов"""
        clicks = clicks_data.get("clicks", 0)
        start_time = clicks_data.get("start_time", time.time())
        end_time = clicks_data.get("end_time", time.time())
        
        # Рассчитываем время игры
        actual_duration = end_time - start_time
        
        # Проверяем валидность времени
        if abs(actual_duration - self.game_duration) > 1.0:  # допуск 1 секунда
            return ClickerGameResult(
                clicks=clicks,
                time_seconds=actual_duration,
                cps=0,
                score=0,
                is_valid=False
            )
        
        # Рассчитываем CPS
        cps = clicks / actual_duration if actual_duration > 0 else 0
        
        # Проверяем на ботов (слишком высокий или низкий CPS)
        if cps < self.min_cps or cps > self.max_cps:
            return ClickerGameResult(
                clicks=clicks,
                time_seconds=actual_duration,
                cps=cps,
                score=0,
                is_valid=False
            )
        
        # Рассчитываем очки (CPS * коэффициент сложности)
        score = cps * 100
        
        return ClickerGameResult(
            clicks=clicks,
            time_seconds=actual_duration,
            cps=cps,
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
    <title>Кликер</title>
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
        
        .timer {
            font-size: 48px;
            font-weight: bold;
            color: #e74c3c;
            margin: 20px 0;
        }
        
        .click-area {
            width: 200px;
            height: 200px;
            background: #3498db;
            border-radius: 50%;
            margin: 20px auto;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            font-weight: bold;
            transition: all 0.1s;
            user-select: none;
        }
        
        .click-area:hover {
            background: #2980b9;
            transform: scale(1.05);
        }
        
        .click-area:active {
            transform: scale(0.95);
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
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .stat-label {
            font-size: 14px;
            color: #7f8c8d;
        }
        
        .start-btn {
            background: #27ae60;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
            margin: 20px 0;
        }
        
        .start-btn:hover {
            background: #229954;
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
    </style>
</head>
<body>
    <div class="game-container">
        <div class="title">🎯 Кликер</div>
        
        <div id="game-area">
            <div class="timer" id="timer">10</div>
            <div class="click-area" id="clickArea">КЛИКАЙ!</div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-value" id="clicks">0</div>
                    <div class="stat-label">Кликов</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="cps">0.0</div>
                    <div class="stat-label">CPS</div>
                </div>
            </div>
            
            <button class="start-btn" id="startBtn">Начать игру</button>
        </div>
        
        <div id="game-over" class="game-over">
            <div class="final-score" id="finalScore">0</div>
            <div>Кликов: <span id="finalClicks">0</span></div>
            <div>CPS: <span id="finalCps">0.0</span></div>
            <button class="start-btn" onclick="location.reload()">Играть снова</button>
        </div>
    </div>

    <script>
        let gameStarted = false;
        let gameEnded = false;
        let clicks = 0;
        let startTime = 0;
        let timerInterval;
        
        const timer = document.getElementById('timer');
        const clickArea = document.getElementById('clickArea');
        const startBtn = document.getElementById('startBtn');
        const clicksDisplay = document.getElementById('clicks');
        const cpsDisplay = document.getElementById('cps');
        const gameArea = document.getElementById('game-area');
        const gameOver = document.getElementById('game-over');
        const finalScore = document.getElementById('finalScore');
        const finalClicks = document.getElementById('finalClicks');
        const finalCps = document.getElementById('finalCps');
        
        function startGame() {
            gameStarted = true;
            gameEnded = false;
            clicks = 0;
            startTime = Date.now();
            startBtn.disabled = true;
            
            let timeLeft = 10;
            timerInterval = setInterval(() => {
                timeLeft--;
                timer.textContent = timeLeft;
                
                if (timeLeft <= 0) {
                    endGame();
                }
            }, 1000);
            
            updateDisplay();
        }
        
        function endGame() {
            if (gameEnded) return;
            
            gameEnded = true;
            clearInterval(timerInterval);
            
            const endTime = Date.now();
            const duration = (endTime - startTime) / 1000;
            const cps = clicks / duration;
            
            // Показываем результаты
            finalClicks.textContent = clicks;
            finalCps.textContent = cps.toFixed(2);
            finalScore.textContent = Math.round(cps * 100);
            
            gameArea.style.display = 'none';
            gameOver.style.display = 'block';
            
            // Отправляем результаты в Telegram
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.sendData(JSON.stringify({
                    clicks: clicks,
                    start_time: startTime / 1000,
                    end_time: endTime / 1000,
                    cps: cps,
                    score: Math.round(cps * 100)
                }));
            }
        }
        
        function handleClick() {
            if (!gameStarted || gameEnded) return;
            
            clicks++;
            updateDisplay();
            
            // Анимация клика
            clickArea.style.transform = 'scale(0.9)';
            setTimeout(() => {
                clickArea.style.transform = 'scale(1)';
            }, 100);
        }
        
        function updateDisplay() {
            clicksDisplay.textContent = clicks;
            
            if (gameStarted && !gameEnded) {
                const currentTime = Date.now();
                const elapsed = (currentTime - startTime) / 1000;
                const currentCps = clicks / elapsed;
                cpsDisplay.textContent = currentCps.toFixed(1);
            }
        }
        
        // Обработчики событий
        startBtn.addEventListener('click', startGame);
        clickArea.addEventListener('click', handleClick);
        
        // Предотвращаем контекстное меню
        clickArea.addEventListener('contextmenu', (e) => e.preventDefault());
        
        // Инициализация Telegram WebApp
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
        }
    </script>
</body>
</html>
        """
