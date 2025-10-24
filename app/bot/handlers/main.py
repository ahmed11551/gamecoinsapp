"""
Основные обработчики команд
"""
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import User, Transaction, TransactionType, TransactionStatus
from app.bot.keyboards import (
    get_main_menu_keyboard, get_games_menu_keyboard, 
    get_tournament_types_keyboard, get_profile_keyboard
)
from app.services.user_service import UserService
from app.services.payment_service import PaymentService

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик команды /start"""
    user_service = UserService(session)
    
    # Проверяем, есть ли пользователь в базе
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    
    if not user:
        # Создаем нового пользователя
        user = await user_service.create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        
        welcome_text = f"""
🎉 <b>Добро пожаловать в Tournament Platform!</b>

Привет, {message.from_user.first_name}! 

🏆 Это платформа для проведения турниров в играх на навыки с реальными денежными призами.

✅ <b>Что разрешено:</b>
• Игры на навыки (шахматы, нарды, кликер, реакция)
• Честные соревнования
• Прозрачные выплаты

❌ <b>Что запрещено:</b>
• Азартные игры
• Игры на удачу

💰 <b>Ваш стартовый баланс:</b> 0 ₽
🎁 <b>Бонус за регистрацию:</b> 100 ₽

Нажмите /deposit для пополнения баланса и начала игры!
        """
        
        # Начисляем бонус за регистрацию
        await user_service.add_transaction(
            user_id=user.id,
            amount=100.0,
            transaction_type=TransactionType.REFERRAL_BONUS,
            description="Бонус за регистрацию"
        )
        
    else:
        welcome_text = f"""
👋 <b>С возвращением, {user.first_name}!</b>

💰 <b>Ваш баланс:</b> {user.balance} ₽
🏆 <b>Рейтинг:</b> {user.rating}
🎮 <b>Игр сыграно:</b> {user.games_played}
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )
    
    # Очищаем состояние
    await state.clear()


@router.message(F.text == "🎮 Игры")
async def show_games_menu(message: Message):
    """Показать меню игр"""
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


@router.message(F.text == "🏆 Турниры")
async def show_tournaments_menu(message: Message):
    """Показать меню турниров"""
    text = """
🏆 <b>Типы турниров:</b>

⚔️ <b>Дуэли (1vs1)</b>
• Быстрые поединки
• Взнос: 100-1000 ₽
• Приз: 90% от взноса

👥 <b>Групповые (8-16 человек)</b>
• Турнирная сетка
• Взнос: 50-200 ₽
• Призы: 1-е место 50%, 2-е 30%, 3-е 20%

🏃 <b>Марафоны (24 часа)</b>
• Длительные соревнования
• Взнос: 100-200 ₽
• Призы: топ-10 участников
    """
    
    await message.answer(text, reply_markup=get_tournament_types_keyboard())


@router.message(F.text == "💰 Баланс")
async def show_balance(message: Message, session: AsyncSession):
    """Показать баланс пользователя"""
    user_service = UserService(session)
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    
    if not user:
        await message.answer("❌ Пользователь не найден. Используйте /start")
        return
    
    # Получаем последние транзакции
    recent_transactions = await user_service.get_recent_transactions(user.id, limit=5)
    
    text = f"""
💰 <b>Ваш баланс:</b> {user.balance} ₽

📊 <b>Статистика:</b>
• Пополнено: {user.total_deposits} ₽
• Выведено: {user.total_withdrawals} ₽
• Выиграно: {user.total_winnings} ₽

📋 <b>Последние операции:</b>
    """
    
    if recent_transactions:
        for transaction in recent_transactions:
            status_emoji = "✅" if transaction.status == TransactionStatus.COMPLETED else "⏳"
            text += f"\n{status_emoji} {transaction.amount} ₽ - {transaction.description}"
    else:
        text += "\nНет операций"
    
    text += "\n\n💡 Используйте /deposit для пополнения или /withdraw для вывода"
    
    await message.answer(text)


@router.message(F.text == "👤 Профиль")
async def show_profile(message: Message, session: AsyncSession):
    """Показать профиль пользователя"""
    user_service = UserService(session)
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    
    if not user:
        await message.answer("❌ Пользователь не найден. Используйте /start")
        return
    
    # Статус верификации
    verification_status = "✅ Верифицирован" if user.is_verified else "❌ Не верифицирован"
    premium_status = "⭐ Премиум" if user.is_premium else "🔒 Обычный"
    
    text = f"""
👤 <b>Профиль пользователя</b>

👤 <b>Имя:</b> {user.first_name} {user.last_name or ''}
🆔 <b>ID:</b> {user.telegram_id}
📅 <b>Регистрация:</b> {user.created_at.strftime('%d.%m.%Y')}
{verification_status}
{premium_status}

🏆 <b>Статистика:</b>
• Рейтинг: {user.rating}
• Игр сыграно: {user.games_played}
• Игр выиграно: {user.games_won}
• Турниров сыграно: {user.tournaments_played}
• Турниров выиграно: {user.tournaments_won}

💰 <b>Финансы:</b>
• Баланс: {user.balance} ₽
• Всего выиграно: {user.total_winnings} ₽
    """
    
    await message.answer(text, reply_markup=get_profile_keyboard())


@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message, session: AsyncSession):
    """Показать статистику"""
    user_service = UserService(session)
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    
    if not user:
        await message.answer("❌ Пользователь не найден. Используйте /start")
        return
    
    # Расчет процента побед
    win_rate = (user.games_won / user.games_played * 100) if user.games_played > 0 else 0
    tournament_win_rate = (user.tournaments_won / user.tournaments_played * 100) if user.tournaments_played > 0 else 0
    
    text = f"""
📊 <b>Ваша статистика</b>

🎮 <b>Игры:</b>
• Сыграно: {user.games_played}
• Выиграно: {user.games_won}
• Процент побед: {win_rate:.1f}%

🏆 <b>Турниры:</b>
• Сыграно: {user.tournaments_played}
• Выиграно: {user.tournaments_won}
• Процент побед: {tournament_win_rate:.1f}%

💰 <b>Финансы:</b>
• Всего пополнено: {user.total_deposits} ₽
• Всего выведено: {user.total_withdrawals} ₽
• Чистый доход: {user.total_winnings - user.total_deposits:.2f} ₽

🏅 <b>Рейтинг:</b> {user.rating}
    """
    
    await message.answer(text)


@router.message(F.text == "❓ Помощь")
async def show_help(message: Message):
    """Показать помощь"""
    text = """
❓ <b>Помощь и поддержка</b>

🤖 <b>Основные команды:</b>
/start - Начать работу с ботом
/profile - Ваш профиль
/balance - Баланс и транзакции
/deposit - Пополнить баланс
/withdraw - Вывести средства
/tournaments - Активные турниры
/help - Эта справка

🎮 <b>Как играть:</b>
1. Пополните баланс через /deposit
2. Выберите игру в меню "🎮 Игры"
3. Участвуйте в турнирах
4. Выигрывайте призы!

💰 <b>Платежи:</b>
• Telegram Stars (основной метод)
• Банковские карты (ЮKassa)
• Криптовалюта (USDT)

⚠️ <b>Важно:</b>
• Минимальная сумма вывода: 500 ₽
• Комиссия на вывод: 3%
• Все игры основаны на навыках

📞 <b>Поддержка:</b>
@support_username - для вопросов
    """
    
    await message.answer(text)


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_games")
async def back_to_games(callback: CallbackQuery):
    """Возврат к играм"""
    await callback.message.edit_text(
        "🎮 <b>Выберите игру:</b>",
        reply_markup=get_games_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_tournaments")
async def back_to_tournaments(callback: CallbackQuery):
    """Возврат к турнирам"""
    await callback.message.edit_text(
        "🏆 <b>Типы турниров:</b>",
        reply_markup=get_tournament_types_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_balance")
async def back_to_balance(callback: CallbackQuery):
    """Возврат к балансу"""
    await callback.message.edit_text(
        "💰 <b>Управление балансом</b>\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()
