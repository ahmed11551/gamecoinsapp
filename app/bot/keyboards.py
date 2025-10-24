"""
Клавиатуры для бота
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню"""
    builder = ReplyKeyboardBuilder()
    
    builder.add(
        KeyboardButton(text="🎮 Игры"),
        KeyboardButton(text="🏆 Турниры"),
        KeyboardButton(text="💰 Баланс"),
        KeyboardButton(text="👤 Профиль")
    )
    builder.add(
        KeyboardButton(text="📊 Статистика"),
        KeyboardButton(text="🎁 Рефералы"),
        KeyboardButton(text="⚙️ Настройки"),
        KeyboardButton(text="❓ Помощь")
    )
    
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup(resize_keyboard=True)


def get_games_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню игр"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="👆 Кликер", callback_data="game_clicker"),
        InlineKeyboardButton(text="⚡ Реакция", callback_data="game_reaction"),
        InlineKeyboardButton(text="🧩 2048", callback_data="game_2048"),
        InlineKeyboardButton(text="♟️ Шахматы", callback_data="game_chess"),
        InlineKeyboardButton(text="🎲 Нарды", callback_data="game_backgammon"),
        InlineKeyboardButton(text="🔍 Сапер", callback_data="game_minesweeper")
    )
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    builder.adjust(2, 2, 2)
    return builder.as_markup()


def get_tournament_types_keyboard() -> InlineKeyboardMarkup:
    """Типы турниров"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="⚔️ Дуэль (1vs1)", callback_data="tournament_duel"),
        InlineKeyboardButton(text="👥 Групповой (8-16)", callback_data="tournament_group"),
        InlineKeyboardButton(text="🏃 Марафон (24ч)", callback_data="tournament_marathon")
    )
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    builder.adjust(1)
    return builder.as_markup()


def get_tournament_fees_keyboard(tournament_type: str) -> InlineKeyboardMarkup:
    """Размеры взносов для турниров"""
    builder = InlineKeyboardBuilder()
    
    if tournament_type == "duel":
        fees = [100, 500, 1000]
    elif tournament_type == "group":
        fees = [50, 100, 200]
    else:  # marathon
        fees = [100, 200]
    
    for fee in fees:
        builder.add(InlineKeyboardButton(
            text=f"{fee} ₽", 
            callback_data=f"tournament_fee_{fee}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_tournaments"))
    builder.adjust(2)
    return builder.as_markup()


def get_payment_methods_keyboard() -> InlineKeyboardMarkup:
    """Методы пополнения"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="⭐ Telegram Stars", callback_data="payment_stars"),
        InlineKeyboardButton(text="💳 Банковская карта", callback_data="payment_card"),
        InlineKeyboardButton(text="₿ Криптовалюта", callback_data="payment_crypto")
    )
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_balance"))
    builder.adjust(1)
    return builder.as_markup()


def get_confirmation_keyboard(action: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{action}"),
        InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_{action}")
    )
    
    builder.adjust(2)
    return builder.as_markup()


def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура профиля"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="📊 Статистика", callback_data="profile_stats"),
        InlineKeyboardButton(text="💰 Транзакции", callback_data="profile_transactions"),
        InlineKeyboardButton(text="🏆 Турниры", callback_data="profile_tournaments"),
        InlineKeyboardButton(text="🎁 Рефералы", callback_data="profile_referrals")
    )
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    builder.adjust(2)
    return builder.as_markup()


def get_game_difficulty_keyboard(game_type: str) -> InlineKeyboardMarkup:
    """Уровни сложности для игр"""
    builder = InlineKeyboardBuilder()
    
    if game_type == "minesweeper":
        difficulties = [
            ("🟢 Легкий", "easy"),
            ("🟡 Средний", "medium"),
            ("🔴 Сложный", "hard")
        ]
    else:
        difficulties = [
            ("🟢 Новичок", "beginner"),
            ("🟡 Любитель", "intermediate"),
            ("🔴 Профи", "expert")
        ]
    
    for text, level in difficulties:
        builder.add(InlineKeyboardButton(
            text=text, 
            callback_data=f"game_difficulty_{game_type}_{level}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_games"))
    builder.adjust(1)
    return builder.as_markup()


def get_tournament_join_keyboard(tournament_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для участия в турнире"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="🎯 Участвовать", callback_data=f"join_tournament_{tournament_id}"),
        InlineKeyboardButton(text="👀 Смотреть", callback_data=f"watch_tournament_{tournament_id}")
    )
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_tournaments"))
    builder.adjust(1)
    return builder.as_markup()


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Админская клавиатура"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"),
        InlineKeyboardButton(text="🏆 Турниры", callback_data="admin_tournaments"),
        InlineKeyboardButton(text="💰 Транзакции", callback_data="admin_transactions"),
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton(text="🔧 Настройки", callback_data="admin_settings"),
        InlineKeyboardButton(text="📢 Рассылка", callback_data="admin_broadcast")
    )
    
    builder.adjust(2)
    return builder.as_markup()
