"""
Регистрация обработчиков
"""
from aiogram import Dispatcher

from app.bot.handlers import main, games, payments, tournaments


def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков"""
    dp.include_router(main.router)
    dp.include_router(games.router)
    dp.include_router(payments.router)
    dp.include_router(tournaments.router)