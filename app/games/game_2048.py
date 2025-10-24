"""
Игра 2048
"""
import random
import time
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class Game2048Result:
    final_score: int
    max_tile: int
    moves_count: int
    time_seconds: float
    is_valid: bool


class Game2048:
    def __init__(self):
        self.board_size = 4
        self.target_tile = 2048
        self.max_time = 300  # 5 минут
        
    def start_game(self) -> Dict[str, Any]:
        """Начать игру"""
        board = self._create_empty_board()
        board = self._add_random_tile(board)
        board = self._add_random_tile(board)
        
        return {
            "game_type": "2048",
            "board": board,
            "score": 0,
            "moves": 0,
            "max_tile": 2,
            "start_time": time.time(),
            "instructions": "Используйте стрелки для перемещения плиток. Цель: получить плитку 2048!"
        }
    
    def process_move(self, game_state: Dict[str, Any], direction: str) -> Dict[str, Any]:
        """Обработать ход"""
        board = game_state["board"]
        score = game_state["score"]
        moves = game_state["moves"]
        max_tile = game_state["max_tile"]
        
        # Сохраняем предыдущее состояние для проверки изменений
        old_board = [row[:] for row in board]
        
        # Выполняем ход
        if direction == "up":
            board, move_score = self._move_up(board)
        elif direction == "down":
            board, move_score = self._move_down(board)
        elif direction == "left":
            board, move_score = self._move_left(board)
        elif direction == "right":
            board, move_score = self._move_right(board)
        else:
            return game_state
        
        # Проверяем, изменилась ли доска
        if board == old_board:
            return game_state  # Ход не изменил доску
        
        # Обновляем счет и количество ходов
        score += move_score
        moves += 1
        
        # Добавляем новую плитку
        board = self._add_random_tile(board)
        
        # Обновляем максимальную плитку
        max_tile = max(max(row) for row in board)
        
        # Проверяем условия окончания игры
        game_over = self._is_game_over(board)
        won = max_tile >= self.target_tile
        
        return {
            "board": board,
            "score": score,
            "moves": moves,
            "max_tile": max_tile,
            "game_over": game_over,
            "won": won,
            "start_time": game_state["start_time"]
        }
    
    def process_results(self, game_state: Dict[str, Any]) -> Game2048Result:
        """Обработать результаты игры"""
        score = game_state["score"]
        max_tile = game_state["max_tile"]
        moves = game_state["moves"]
        start_time = game_state["start_time"]
        end_time = time.time()
        
        # Проверяем валидность времени игры
        duration = end_time - start_time
        if duration > self.max_time:
            return Game2048Result(
                final_score=0,
                max_tile=0,
                moves_count=0,
                time_seconds=duration,
                is_valid=False
            )
        
        # Рассчитываем очки
        final_score = score + (max_tile * 10) + (moves * 5)
        
        return Game2048Result(
            final_score=final_score,
            max_tile=max_tile,
            moves_count=moves,
            time_seconds=duration,
            is_valid=True
        )
    
    def _create_empty_board(self) -> List[List[int]]:
        """Создать пустую доску"""
        return [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
    
    def _add_random_tile(self, board: List[List[int]]) -> List[List[int]]:
        """Добавить случайную плитку (2 или 4)"""
        empty_cells = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = random.choice([2, 4])
        
        return board
    
    def _move_left(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
        """Движение влево"""
        new_board = []
        score = 0
        
        for row in board:
            # Убираем нули
            non_zero = [cell for cell in row if cell != 0]
            
            # Объединяем одинаковые плитки
            merged = []
            i = 0
            while i < len(non_zero):
                if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
                    merged.append(non_zero[i] * 2)
                    score += non_zero[i] * 2
                    i += 2
                else:
                    merged.append(non_zero[i])
                    i += 1
            
            # Дополняем нулями
            while len(merged) < self.board_size:
                merged.append(0)
            
            new_board.append(merged)
        
        return new_board, score
    
    def _move_right(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
        """Движение вправо"""
        new_board = []
        score = 0
        
        for row in board:
            # Убираем нули
            non_zero = [cell for cell in row if cell != 0]
            
            # Объединяем одинаковые плитки
            merged = []
            i = len(non_zero) - 1
            while i >= 0:
                if i > 0 and non_zero[i] == non_zero[i - 1]:
                    merged.insert(0, non_zero[i] * 2)
                    score += non_zero[i] * 2
                    i -= 2
                else:
                    merged.insert(0, non_zero[i])
                    i -= 1
            
            # Дополняем нулями
            while len(merged) < self.board_size:
                merged.insert(0, 0)
            
            new_board.append(merged)
        
        return new_board, score
    
    def _move_up(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
        """Движение вверх"""
        # Транспонируем, двигаем влево, транспонируем обратно
        transposed = list(zip(*board))
        moved, score = self._move_left([list(row) for row in transposed])
        return list(zip(*moved)), score
    
    def _move_down(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
        """Движение вниз"""
        # Транспонируем, двигаем вправо, транспонируем обратно
        transposed = list(zip(*board))
        moved, score = self._move_right([list(row) for row in transposed])
        return list(zip(*moved)), score
    
    def _is_game_over(self, board: List[List[int]]) -> bool:
        """Проверить, окончена ли игра"""
        # Проверяем наличие пустых клеток
        for row in board:
            if 0 in row:
                return False
        
        # Проверяем возможность объединения
        for i in range(self.board_size):
            for j in range(self.board_size):
                current = board[i][j]
                
                # Проверяем соседние клетки
                if (i < self.board_size - 1 and board[i + 1][j] == current) or \
                   (j < self.board_size - 1 and board[i][j + 1] == current):
                    return False
        
        return True
    
    def generate_webview_html(self) -> str:
        """Генерировать HTML для WebView"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2048</title>
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
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 400px;
            margin: 0 auto;
        }
        
        .title {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
        
        .score-container {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        
        .score-box {
            background: #bbada0;
            color: white;
            padding: 10px;
            border-radius: 5px;
            min-width: 80px;
        }
        
        .score-label {
            font-size: 12px;
            text-transform: uppercase;
        }
        
        .score-value {
            font-size: 18px;
            font-weight: bold;
        }
        
        .game-board {
            background: #bbada0;
            border-radius: 10px;
            padding: 10px;
            margin: 20px 0;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-gap: 10px;
            width: 100%;
            max-width: 300px;
            margin: 0 auto;
        }
        
        .cell {
            background: rgba(238, 228, 218, 0.35);
            border-radius: 5px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            color: #776e65;
        }
        
        .cell-2 { background: #eee4da; color: #776e65; }
        .cell-4 { background: #ede0c8; color: #776e65; }
        .cell-8 { background: #f2b179; color: #f9f6f2; }
        .cell-16 { background: #f59563; color: #f9f6f2; }
        .cell-32 { background: #f67c5f; color: #f9f6f2; }
        .cell-64 { background: #f65e3b; color: #f9f6f2; }
        .cell-128 { background: #edcf72; color: #f9f6f2; font-size: 20px; }
        .cell-256 { background: #edcc61; color: #f9f6f2; font-size: 20px; }
        .cell-512 { background: #edc850; color: #f9f6f2; font-size: 20px; }
        .cell-1024 { background: #edc53f; color: #f9f6f2; font-size: 18px; }
        .cell-2048 { background: #edc22e; color: #f9f6f2; font-size: 18px; }
        
        .controls {
            margin: 20px 0;
        }
        
        .control-btn {
            background: #8f7a66;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            margin: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .control-btn:hover {
            background: #9f8a76;
        }
        
        .control-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .game-over {
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.8);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 20px;
        }
        
        .game-over.show {
            display: flex;
        }
        
        .final-score {
            font-size: 32px;
            margin: 20px 0;
        }
        
        .instructions {
            font-size: 14px;
            color: #666;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <div class="title">🧩 2048</div>
        
        <div class="score-container">
            <div class="score-box">
                <div class="score-label">Счет</div>
                <div class="score-value" id="score">0</div>
            </div>
            <div class="score-box">
                <div class="score-label">Ходы</div>
                <div class="score-value" id="moves">0</div>
            </div>
            <div class="score-box">
                <div class="score-label">Макс</div>
                <div class="score-value" id="maxTile">2</div>
            </div>
        </div>
        
        <div class="game-board">
            <div class="grid" id="grid"></div>
        </div>
        
        <div class="controls">
            <button class="control-btn" id="newGameBtn">Новая игра</button>
            <button class="control-btn" id="undoBtn" disabled>Отменить</button>
        </div>
        
        <div class="instructions">
            Используйте стрелки на клавиатуре или кнопки ниже для управления
        </div>
        
        <div class="controls">
            <button class="control-btn" id="upBtn">↑</button>
            <div>
                <button class="control-btn" id="leftBtn">←</button>
                <button class="control-btn" id="rightBtn">→</button>
            </div>
            <button class="control-btn" id="downBtn">↓</button>
        </div>
        
        <div class="game-over" id="gameOver">
            <div class="final-score" id="finalScore">0</div>
            <div id="gameOverText">Игра окончена!</div>
            <button class="control-btn" onclick="location.reload()">Играть снова</button>
        </div>
    </div>

    <script>
        let board = [];
        let score = 0;
        let moves = 0;
        let maxTile = 2;
        let gameOver = false;
        let won = false;
        let startTime = Date.now();
        
        const grid = document.getElementById('grid');
        const scoreElement = document.getElementById('score');
        const movesElement = document.getElementById('moves');
        const maxTileElement = document.getElementById('maxTile');
        const gameOverDiv = document.getElementById('gameOver');
        const finalScoreElement = document.getElementById('finalScore');
        const gameOverText = document.getElementById('gameOverText');
        
        function initGame() {
            board = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ];
            score = 0;
            moves = 0;
            maxTile = 2;
            gameOver = false;
            won = false;
            startTime = Date.now();
            
            addRandomTile();
            addRandomTile();
            updateDisplay();
        }
        
        function addRandomTile() {
            const emptyCells = [];
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (board[i][j] === 0) {
                        emptyCells.push({row: i, col: j});
                    }
                }
            }
            
            if (emptyCells.length > 0) {
                const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
                board[randomCell.row][randomCell.col] = Math.random() < 0.9 ? 2 : 4;
            }
        }
        
        function updateDisplay() {
            grid.innerHTML = '';
            
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    
                    if (board[i][j] !== 0) {
                        cell.textContent = board[i][j];
                        cell.classList.add(`cell-${board[i][j]}`);
                    }
                    
                    grid.appendChild(cell);
                }
            }
            
            scoreElement.textContent = score;
            movesElement.textContent = moves;
            maxTileElement.textContent = maxTile;
        }
        
        function moveLeft() {
            let moved = false;
            let moveScore = 0;
            
            for (let i = 0; i < 4; i++) {
                const row = board[i].filter(cell => cell !== 0);
                const newRow = [];
                
                for (let j = 0; j < row.length; j++) {
                    if (j < row.length - 1 && row[j] === row[j + 1]) {
                        newRow.push(row[j] * 2);
                        moveScore += row[j] * 2;
                        j++;
                    } else {
                        newRow.push(row[j]);
                    }
                }
                
                while (newRow.length < 4) {
                    newRow.push(0);
                }
                
                if (JSON.stringify(newRow) !== JSON.stringify(board[i])) {
                    moved = true;
                }
                
                board[i] = newRow;
            }
            
            if (moved) {
                score += moveScore;
                moves++;
                addRandomTile();
                updateMaxTile();
                updateDisplay();
                checkGameOver();
            }
        }
        
        function moveRight() {
            let moved = false;
            let moveScore = 0;
            
            for (let i = 0; i < 4; i++) {
                const row = board[i].filter(cell => cell !== 0);
                const newRow = [];
                
                for (let j = row.length - 1; j >= 0; j--) {
                    if (j > 0 && row[j] === row[j - 1]) {
                        newRow.unshift(row[j] * 2);
                        moveScore += row[j] * 2;
                        j--;
                    } else {
                        newRow.unshift(row[j]);
                    }
                }
                
                while (newRow.length < 4) {
                    newRow.unshift(0);
                }
                
                if (JSON.stringify(newRow) !== JSON.stringify(board[i])) {
                    moved = true;
                }
                
                board[i] = newRow;
            }
            
            if (moved) {
                score += moveScore;
                moves++;
                addRandomTile();
                updateMaxTile();
                updateDisplay();
                checkGameOver();
            }
        }
        
        function moveUp() {
            let moved = false;
            let moveScore = 0;
            
            for (let j = 0; j < 4; j++) {
                const column = [];
                for (let i = 0; i < 4; i++) {
                    if (board[i][j] !== 0) {
                        column.push(board[i][j]);
                    }
                }
                
                const newColumn = [];
                for (let i = 0; i < column.length; i++) {
                    if (i < column.length - 1 && column[i] === column[i + 1]) {
                        newColumn.push(column[i] * 2);
                        moveScore += column[i] * 2;
                        i++;
                    } else {
                        newColumn.push(column[i]);
                    }
                }
                
                while (newColumn.length < 4) {
                    newColumn.push(0);
                }
                
                for (let i = 0; i < 4; i++) {
                    if (board[i][j] !== newColumn[i]) {
                        moved = true;
                    }
                    board[i][j] = newColumn[i];
                }
            }
            
            if (moved) {
                score += moveScore;
                moves++;
                addRandomTile();
                updateMaxTile();
                updateDisplay();
                checkGameOver();
            }
        }
        
        function moveDown() {
            let moved = false;
            let moveScore = 0;
            
            for (let j = 0; j < 4; j++) {
                const column = [];
                for (let i = 0; i < 4; i++) {
                    if (board[i][j] !== 0) {
                        column.push(board[i][j]);
                    }
                }
                
                const newColumn = [];
                for (let i = column.length - 1; i >= 0; i--) {
                    if (i > 0 && column[i] === column[i - 1]) {
                        newColumn.unshift(column[i] * 2);
                        moveScore += column[i] * 2;
                        i--;
                    } else {
                        newColumn.unshift(column[i]);
                    }
                }
                
                while (newColumn.length < 4) {
                    newColumn.unshift(0);
                }
                
                for (let i = 0; i < 4; i++) {
                    if (board[i][j] !== newColumn[i]) {
                        moved = true;
                    }
                    board[i][j] = newColumn[i];
                }
            }
            
            if (moved) {
                score += moveScore;
                moves++;
                addRandomTile();
                updateMaxTile();
                updateDisplay();
                checkGameOver();
            }
        }
        
        function updateMaxTile() {
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (board[i][j] > maxTile) {
                        maxTile = board[i][j];
                    }
                }
            }
        }
        
        function checkGameOver() {
            // Проверяем победу
            if (maxTile >= 2048 && !won) {
                won = true;
                gameOverText.textContent = 'Поздравляем! Вы получили 2048!';
                showGameOver();
                return;
            }
            
            // Проверяем поражение
            let hasEmpty = false;
            let canMove = false;
            
            for (let i = 0; i < 4; i++) {
                for (let j = 0; j < 4; j++) {
                    if (board[i][j] === 0) {
                        hasEmpty = true;
                    }
                    
                    if (i < 3 && board[i][j] === board[i + 1][j]) {
                        canMove = true;
                    }
                    if (j < 3 && board[i][j] === board[i][j + 1]) {
                        canMove = true;
                    }
                }
            }
            
            if (!hasEmpty && !canMove) {
                gameOver = true;
                gameOverText.textContent = 'Игра окончена!';
                showGameOver();
            }
        }
        
        function showGameOver() {
            const finalScore = score + (maxTile * 10) + (moves * 5);
            finalScoreElement.textContent = finalScore;
            gameOverDiv.classList.add('show');
            
            // Отправляем результаты в Telegram
            if (window.Telegram && window.Telegram.WebApp) {
                window.Telegram.WebApp.sendData(JSON.stringify({
                    score: score,
                    max_tile: maxTile,
                    moves: moves,
                    final_score: finalScore,
                    time_seconds: (Date.now() - startTime) / 1000,
                    won: won
                }));
            }
        }
        
        // Обработчики событий
        document.getElementById('newGameBtn').addEventListener('click', initGame);
        document.getElementById('upBtn').addEventListener('click', moveUp);
        document.getElementById('downBtn').addEventListener('click', moveDown);
        document.getElementById('leftBtn').addEventListener('click', moveLeft);
        document.getElementById('rightBtn').addEventListener('click', moveRight);
        
        // Обработка клавиатуры
        document.addEventListener('keydown', (e) => {
            if (gameOver) return;
            
            switch(e.key) {
                case 'ArrowUp':
                    e.preventDefault();
                    moveUp();
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    moveDown();
                    break;
                case 'ArrowLeft':
                    e.preventDefault();
                    moveLeft();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    moveRight();
                    break;
            }
        });
        
        // Инициализация Telegram WebApp
        if (window.Telegram && window.Telegram.WebApp) {
            window.Telegram.WebApp.ready();
            window.Telegram.WebApp.expand();
        }
        
        // Начинаем игру
        initGame();
    </script>
</body>
</html>
        """
