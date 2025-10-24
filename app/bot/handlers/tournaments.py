"""
Обработчики турниров
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import (
    get_tournament_types_keyboard, get_tournament_fees_keyboard,
    get_tournament_join_keyboard, get_main_menu_keyboard
)
from app.bot.states import TournamentCreation
from app.services.tournament_service import TournamentService
from app.services.user_service import UserService
from app.database.models import GameType, TournamentType

router = Router()
logger = logging.getLogger(__name__)


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


@router.callback_query(F.data.startswith("tournament_"))
async def handle_tournament_type(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора типа турнира"""
    tournament_type = callback.data.split("_")[1]
    
    if tournament_type in ["duel", "group", "marathon"]:
        await state.update_data(tournament_type=tournament_type)
        await callback.message.edit_text(
            f"🏆 <b>Выберите размер взноса для {tournament_type}:</b>",
            reply_markup=get_tournament_fees_keyboard(tournament_type)
        )
    else:
        await callback.answer("❌ Неизвестный тип турнира")
    
    await callback.answer()


@router.callback_query(F.data.startswith("tournament_fee_"))
async def handle_tournament_fee(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработчик выбора размера взноса"""
    try:
        fee = int(callback.data.split("_")[2])
        data = await state.get_data()
        tournament_type = data.get("tournament_type")
        
        await state.update_data(entry_fee=fee)
        
        # Показываем доступные игры для этого типа турнира
        if tournament_type == "duel":
            games = ["clicker", "reaction", "2048"]
        elif tournament_type == "group":
            games = ["clicker", "reaction", "2048", "chess", "backgammon"]
        else:  # marathon
            games = ["2048", "chess", "backgammon"]
        
        text = f"""
🏆 <b>Создание турнира</b>

📋 <b>Тип:</b> {tournament_type.capitalize()}
💰 <b>Взнос:</b> {fee} ₽

Выберите игру:
        """
        
        keyboard = InlineKeyboardBuilder()
        for game in games:
            keyboard.add(InlineKeyboardButton(
                text=f"🎮 {game.capitalize()}", 
                callback_data=f"create_tournament_game_{game}"
            ))
        
        keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_tournaments"))
        keyboard.adjust(2)
        
        await callback.message.edit_text(text, reply_markup=keyboard.as_markup())
        
    except ValueError:
        await callback.answer("❌ Неверный размер взноса")
    
    await callback.answer()


@router.callback_query(F.data.startswith("create_tournament_game_"))
async def handle_tournament_game(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработчик выбора игры для турнира"""
    game_type = callback.data.split("_")[3]
    
    await state.update_data(game_type=game_type)
    await state.set_state(TournamentCreation.waiting_for_title)
    
    text = f"""
🏆 <b>Создание турнира</b>

Введите название турнира:
Пример: "Быстрые дуэли в Кликер"
    """
    
    await callback.message.edit_text(text)
    await callback.answer()


@router.message(TournamentCreation.waiting_for_title)
async def handle_tournament_title(message: Message, state: FSMContext):
    """Обработчик названия турнира"""
    title = message.text.strip()
    
    if len(title) < 3 or len(title) > 100:
        await message.answer("❌ Название должно быть от 3 до 100 символов")
        return
    
    await state.update_data(title=title)
    await state.set_state(TournamentCreation.waiting_for_description)
    
    await message.answer(
        "📝 <b>Введите описание турнира:</b>\n\n"
        "Пример: 'Турнир для быстрых игроков. Победит самый ловкий!'"
    )


@router.message(TournamentCreation.waiting_for_description)
async def handle_tournament_description(message: Message, state: FSMContext):
    """Обработчик описания турнира"""
    description = message.text.strip()
    
    if len(description) > 500:
        await message.answer("❌ Описание не должно превышать 500 символов")
        return
    
    await state.update_data(description=description)
    await state.set_state(TournamentCreation.waiting_for_max_participants)
    
    data = await state.get_data()
    tournament_type = data.get("tournament_type")
    
    if tournament_type == "duel":
        max_participants = 2
        await state.update_data(max_participants=max_participants)
        await show_tournament_confirmation(message, state)
    else:
        await message.answer(
            f"👥 <b>Максимальное количество участников:</b>\n\n"
            f"Введите число от 2 до {'16' if tournament_type == 'group' else '100'}"
        )


@router.message(TournamentCreation.waiting_for_max_participants)
async def handle_max_participants(message: Message, state: FSMContext):
    """Обработчик максимального количества участников"""
    try:
        max_participants = int(message.text)
        data = await state.get_data()
        tournament_type = data.get("tournament_type")
        
        if tournament_type == "group" and (max_participants < 2 or max_participants > 16):
            await message.answer("❌ Для группового турнира: от 2 до 16 участников")
            return
        elif tournament_type == "marathon" and (max_participants < 2 or max_participants > 100):
            await message.answer("❌ Для марафона: от 2 до 100 участников")
            return
        
        await state.update_data(max_participants=max_participants)
        await show_tournament_confirmation(message, state)
        
    except ValueError:
        await message.answer("❌ Введите корректное число")


async def show_tournament_confirmation(message: Message, state: FSMContext):
    """Показать подтверждение создания турнира"""
    data = await state.get_data()
    
    text = f"""
🏆 <b>Подтверждение создания турнира</b>

📋 <b>Название:</b> {data.get('title')}
📝 <b>Описание:</b> {data.get('description')}
🎮 <b>Игра:</b> {data.get('game_type').capitalize()}
⚔️ <b>Тип:</b> {data.get('tournament_type').capitalize()}
💰 <b>Взнос:</b> {data.get('entry_fee')} ₽
👥 <b>Участников:</b> {data.get('max_participants')}

⚠️ <b>Внимание:</b> Турнир начнется автоматически при наборе минимального количества участников.
    """
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="✅ Создать турнир", callback_data="confirm_tournament_creation"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_tournament_creation")
    )
    keyboard.adjust(1)
    
    await message.answer(text, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "confirm_tournament_creation")
async def confirm_tournament_creation(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Подтвердить создание турнира"""
    data = await state.get_data()
    
    tournament_service = TournamentService(session)
    
    # Создаем турнир
    tournament = await tournament_service.create_tournament(
        creator_id=callback.from_user.id,
        title=data.get("title"),
        description=data.get("description"),
        game_type=GameType(data.get("game_type")),
        tournament_type=TournamentType(data.get("tournament_type")),
        entry_fee=data.get("entry_fee"),
        max_participants=data.get("max_participants")
    )
    
    await state.clear()
    
    await callback.message.edit_text(
        f"✅ <b>Турнир создан!</b>\n\n"
        f"🆔 <b>ID:</b> {tournament.id}\n"
        f"📋 <b>Название:</b> {tournament.title}\n"
        f"💰 <b>Взнос:</b> {tournament.entry_fee} ₽\n"
        f"🏆 <b>Призовой фонд:</b> {tournament.prize_pool:.2f} ₽\n\n"
        f"🔗 <b>Ссылка для участия:</b>\n"
        f"<code>https://t.me/your_bot?start=tournament_{tournament.id}</code>\n\n"
        f"Турнир начнется при наборе участников!",
        reply_markup=get_main_menu_keyboard()
    )
    
    await callback.answer()


@router.callback_query(F.data == "cancel_tournament_creation")
async def cancel_tournament_creation(callback: CallbackQuery, state: FSMContext):
    """Отменить создание турнира"""
    await state.clear()
    
    await callback.message.edit_text(
        "❌ <b>Создание турнира отменено</b>\n\n"
        "Вы можете создать новый турнир в любое время.",
        reply_markup=get_main_menu_keyboard()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("join_tournament_"))
async def handle_join_tournament(callback: CallbackQuery, session: AsyncSession):
    """Обработчик участия в турнире"""
    try:
        tournament_id = int(callback.data.split("_")[2])
        
        tournament_service = TournamentService(session)
        
        # Проверяем турнир
        tournament = await tournament_service.get_tournament_by_id(tournament_id)
        
        if not tournament:
            await callback.answer("❌ Турнир не найден")
            return
        
        if tournament.status.value != "registration":
            await callback.answer("❌ Регистрация на турнир закрыта")
            return
        
        # Участвуем в турнире
        success = await tournament_service.join_tournament(tournament_id, callback.from_user.id)
        
        if success:
            await callback.message.edit_text(
                f"✅ <b>Вы успешно зарегистрированы!</b>\n\n"
                f"🏆 <b>Турнир:</b> {tournament.title}\n"
                f"💰 <b>Взнос:</b> {tournament.entry_fee} ₽\n"
                f"🎮 <b>Игра:</b> {tournament.game_type.value}\n\n"
                f"Турнир начнется при наборе участников!"
            )
        else:
            await callback.message.edit_text(
                "❌ <b>Не удалось зарегистрироваться</b>\n\n"
                "Возможные причины:\n"
                "• Недостаточно средств на балансе\n"
                "• Турнир уже заполнен\n"
                "• Вы уже участвуете в турнире"
            )
        
    except ValueError:
        await callback.answer("❌ Неверный ID турнира")
    
    await callback.answer()


@router.message(Command("tournaments"))
async def show_active_tournaments(message: Message, session: AsyncSession):
    """Показать активные турниры"""
    tournament_service = TournamentService(session)
    tournaments = await tournament_service.get_active_tournaments()
    
    if not tournaments:
        text = "🏆 <b>Активных турниров нет</b>\n\nСоздайте новый турнир или дождитесь появления доступных соревнований."
    else:
        text = "🏆 <b>Активные турниры:</b>\n\n"
        
        for tournament in tournaments[:10]:  # Показываем только первые 10
            status_emoji = "🟢" if tournament.status.value == "registration" else "🟡"
            participants_count = len(tournament.participants)
            
            text += f"{status_emoji} <b>{tournament.title}</b>\n"
            text += f"🎮 {tournament.game_type.value} • 💰 {tournament.entry_fee} ₽\n"
            text += f"👥 {participants_count}/{tournament.max_participants} участников\n"
            text += f"🏆 Призовой фонд: {tournament.prize_pool:.2f} ₽\n\n"
    
    await message.answer(text)
