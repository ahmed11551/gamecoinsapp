"""
Обработчики игр
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import get_game_difficulty_keyboard, get_main_menu_keyboard
from app.games.clicker import ClickerGame
from app.games.reaction import ReactionTestGame
from app.games.game_2048 import Game2048

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("game_"))
async def handle_game_selection(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора игры"""
    game_type = callback.data.split("_")[1]
    
    if game_type in ["clicker", "reaction", "2048"]:
        # Для простых игр сразу показываем WebView
        await start_simple_game(callback, game_type)
    else:
        # Для сложных игр показываем уровни сложности
        await callback.message.edit_text(
            f"🎮 <b>Выберите уровень сложности для {game_type}:</b>",
            reply_markup=get_game_difficulty_keyboard(game_type)
        )
    
    await callback.answer()


async def start_simple_game(callback: CallbackQuery, game_type: str):
    """Запустить простую игру"""
    if game_type == "clicker":
        game = ClickerGame()
        html_content = game.generate_webview_html()
        title = "👆 Кликер"
        description = "Кликайте как можно быстрее в течение 10 секунд!"
        
    elif game_type == "reaction":
        game = ReactionTestGame()
        html_content = game.generate_webview_html()
        title = "⚡ Тест на реакцию"
        description = "Нажмите кнопку как можно быстрее, когда она станет зеленой!"
        
    elif game_type == "2048":
        game = Game2048()
        html_content = game.generate_webview_html()
        title = "🧩 2048"
        description = "Используйте стрелки для перемещения плиток. Цель: получить плитку 2048!"
        
    else:
        await callback.answer("❌ Неизвестная игра")
        return
    
    # Сохраняем информацию об игре в состоянии
    await state.update_data(
        game_type=game_type,
        game_started=True
    )
    
    await callback.message.edit_text(
        f"{title}\n\n{description}\n\n🎯 Игра откроется в новом окне",
        reply_markup=get_main_menu_keyboard()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("game_difficulty_"))
async def handle_difficulty_selection(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора сложности"""
    parts = callback.data.split("_")
    game_type = parts[2]
    difficulty = parts[3]
    
    await state.update_data(
        game_type=game_type,
        difficulty=difficulty,
        game_started=True
    )
    
    await callback.message.edit_text(
        f"🎮 <b>{game_type.capitalize()} - {difficulty.capitalize()}</b>\n\n"
        f"Игра будет запущена в турнирном режиме.\n"
        f"Выберите турнир для участия:",
        reply_markup=get_main_menu_keyboard()
    )
    
    await callback.answer()


@router.message(F.text == "🎮 Игры")
async def show_games_menu(message: Message):
    """Показать меню игр"""
    from app.bot.keyboards import get_games_menu_keyboard
    
    text = """
🎮 <b>Выберите игру:</b>

👆 <b>Кликер</b> - тест на скорость кликов
⚡ <b>Реакция</b> - тест на скорость реакции  
🧩 <b>2048</b> - логическая головоломка
♟️ <b>Шахматы</b> - классическая игра
🎲 <b>Нарды</b> - стратегическая игра
🔍 <b>Сапер</b> - логическая игра

Все игры основаны на навыках, а не на удаче!
    """
    
    await message.answer(text, reply_markup=get_games_menu_keyboard())
