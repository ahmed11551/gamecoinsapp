"""
Обработчики платежей
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, PreCheckoutQuery, SuccessfulPayment
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards import get_payment_methods_keyboard, get_confirmation_keyboard, get_main_menu_keyboard
from app.bot.states import PaymentStates, WithdrawalStates
from app.services.user_service import UserService
from app.services.payment_service import PaymentService
from app.config import settings

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "💰 Баланс")
async def show_balance_menu(message: Message, session: AsyncSession):
    """Показать меню баланса"""
    user_service = UserService(session)
    user = await user_service.get_user_by_telegram_id(message.from_user.id)
    
    if not user:
        await message.answer("❌ Пользователь не найден. Используйте /start")
        return
    
    text = f"""
💰 <b>Ваш баланс: {user.balance} ₽</b>

📊 <b>Статистика:</b>
• Пополнено: {user.total_deposits} ₽
• Выведено: {user.total_withdrawals} ₽
• Выиграно: {user.total_winnings} ₽

💡 <b>Доступные действия:</b>
• Пополнить баланс
• Вывести средства
• История транзакций
    """
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text="💳 Пополнить", callback_data="deposit_menu"),
        InlineKeyboardButton(text="💸 Вывести", callback_data="withdraw_menu"),
        InlineKeyboardButton(text="📋 История", callback_data="transaction_history")
    )
    keyboard.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    keyboard.adjust(1)
    
    await message.answer(text, reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "deposit_menu")
async def show_deposit_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню пополнения"""
    await state.set_state(PaymentStates.waiting_for_amount)
    
    text = """
💳 <b>Пополнение баланса</b>

Выберите способ пополнения:

⭐ <b>Telegram Stars</b> - мгновенно, без комиссии
💳 <b>Банковская карта</b> - через ЮKassa
₿ <b>Криптовалюта</b> - USDT, анонимно

Минимальная сумма пополнения: 100 ₽
    """
    
    await callback.message.edit_text(text, reply_markup=get_payment_methods_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("payment_"))
async def handle_payment_method(callback: CallbackQuery, state: FSMContext):
    """Обработчик выбора способа платежа"""
    payment_method = callback.data.split("_")[1]
    
    await state.update_data(payment_method=payment_method)
    
    if payment_method == "stars":
        text = """
⭐ <b>Пополнение через Telegram Stars</b>

Введите сумму для пополнения (от 100 ₽):
Пример: 500
        """
    elif payment_method == "card":
        text = """
💳 <b>Пополнение через банковскую карту</b>

Введите сумму для пополнения (от 100 ₽):
Пример: 1000
        """
    else:  # crypto
        text = """
₿ <b>Пополнение через криптовалюту</b>

Введите сумму для пополнения в USDT (от 10 USDT):
Пример: 50
        """
    
    await callback.message.edit_text(text)
    await callback.answer()


@router.message(PaymentStates.waiting_for_amount)
async def handle_deposit_amount(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик суммы пополнения"""
    try:
        amount = float(message.text)
        
        if amount < 100:
            await message.answer("❌ Минимальная сумма пополнения: 100 ₽")
            return
        
        if amount > 50000:
            await message.answer("❌ Максимальная сумма пополнения: 50 000 ₽")
            return
        
        data = await state.get_data()
        payment_method = data.get("payment_method")
        
        if payment_method == "stars":
            await process_telegram_stars_payment(message, amount, session)
        elif payment_method == "card":
            await process_card_payment(message, amount, session)
        else:  # crypto
            await process_crypto_payment(message, amount, session)
        
        await state.clear()
        
    except ValueError:
        await message.answer("❌ Введите корректную сумму (только числа)")


async def process_telegram_stars_payment(message: Message, amount: float, session: AsyncSession):
    """Обработать платеж через Telegram Stars"""
    payment_service = PaymentService(session)
    
    # Создаем запрос на пополнение
    transaction = await payment_service.create_deposit_request(
        user_id=message.from_user.id,
        amount=amount,
        payment_method="telegram_stars"
    )
    
    # Здесь должна быть интеграция с Telegram Stars API
    # Пока что симулируем успешный платеж
    success = await payment_service.process_telegram_stars_payment(
        user_id=message.from_user.id,
        amount=amount,
        external_id=f"stars_{transaction.id}"
    )
    
    if success:
        await message.answer(
            f"✅ <b>Баланс успешно пополнен!</b>\n\n"
            f"💰 Сумма: {amount} ₽\n"
            f"💳 Способ: Telegram Stars\n"
            f"🆔 ID транзакции: {transaction.id}"
        )
    else:
        await message.answer("❌ Ошибка при пополнении баланса. Попробуйте позже.")


async def process_card_payment(message: Message, amount: float, session: AsyncSession):
    """Обработать платеж через карту"""
    payment_service = PaymentService(session)
    
    # Создаем запрос на пополнение
    transaction = await payment_service.create_deposit_request(
        user_id=message.from_user.id,
        amount=amount,
        payment_method="yookassa"
    )
    
    # Здесь должна быть интеграция с ЮKassa
    # Пока что показываем инструкции
    await message.answer(
        f"💳 <b>Пополнение через банковскую карту</b>\n\n"
        f"💰 Сумма: {amount} ₽\n"
        f"🆔 ID транзакции: {transaction.id}\n\n"
        f"📋 <b>Инструкции:</b>\n"
        f"1. Перейдите по ссылке для оплаты\n"
        f"2. Введите данные карты\n"
        f"3. Подтвердите платеж\n"
        f"4. Средства поступят на баланс в течение 5 минут\n\n"
        f"🔗 Ссылка для оплаты: https://yookassa.ru/pay/{transaction.id}\n\n"
        f"⚠️ <b>Важно:</b> Не закрывайте это сообщение до завершения оплаты!"
    )


async def process_crypto_payment(message: Message, amount: float, session: AsyncSession):
    """Обработать платеж через криптовалюту"""
    payment_service = PaymentService(session)
    
    # Создаем запрос на пополнение
    transaction = await payment_service.create_deposit_request(
        user_id=message.from_user.id,
        amount=amount,
        payment_method="crypto_usdt"
    )
    
    # Здесь должна быть интеграция с Binance Pay или другой криптоплатежной системой
    await message.answer(
        f"₿ <b>Пополнение через USDT</b>\n\n"
        f"💰 Сумма: {amount} USDT\n"
        f"🆔 ID транзакции: {transaction.id}\n\n"
        f"📋 <b>Инструкции:</b>\n"
        f"1. Отправьте {amount} USDT на адрес:\n"
        f"<code>TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE</code>\n"
        f"2. В комментарии укажите: {transaction.id}\n"
        f"3. Дождитесь подтверждения (обычно 5-15 минут)\n"
        f"4. Средства поступят на баланс автоматически\n\n"
        f"⚠️ <b>Важно:</b> Отправляйте только USDT (TRC20)!"
    )


@router.callback_query(F.data == "withdraw_menu")
async def show_withdraw_menu(callback: CallbackQuery, state: FSMContext):
    """Показать меню вывода средств"""
    await state.set_state(WithdrawalStates.waiting_for_amount)
    
    text = f"""
💸 <b>Вывод средств</b>

Минимальная сумма вывода: {settings.MIN_WITHDRAWAL_AMOUNT} ₽
Комиссия на вывод: {settings.WITHDRAWAL_COMMISSION * 100}%

Введите сумму для вывода:
    """
    
    await callback.message.edit_text(text)
    await callback.answer()


@router.message(WithdrawalStates.waiting_for_amount)
async def handle_withdrawal_amount(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик суммы вывода"""
    try:
        amount = float(message.text)
        
        if amount < settings.MIN_WITHDRAWAL_AMOUNT:
            await message.answer(f"❌ Минимальная сумма вывода: {settings.MIN_WITHDRAWAL_AMOUNT} ₽")
            return
        
        user_service = UserService(session)
        user = await user_service.get_user_by_telegram_id(message.from_user.id)
        
        if not user or user.balance < amount:
            await message.answer("❌ Недостаточно средств на балансе")
            return
        
        commission = amount * settings.WITHDRAWAL_COMMISSION
        final_amount = amount - commission
        
        await state.update_data(
            withdrawal_amount=amount,
            commission=commission,
            final_amount=final_amount
        )
        
        await state.set_state(WithdrawalStates.waiting_for_payment_details)
        
        text = f"""
💸 <b>Подтверждение вывода</b>

💰 Сумма к выводу: {amount} ₽
💸 Комиссия ({settings.WITHDRAWAL_COMMISSION * 100}%): {commission:.2f} ₽
✅ К получению: {final_amount:.2f} ₽

Введите реквизиты для получения:
• Номер карты (для банковского перевода)
• Или адрес кошелька (для криптовалюты)
        """
        
        await message.answer(text)
        
    except ValueError:
        await message.answer("❌ Введите корректную сумму (только числа)")


@router.message(WithdrawalStates.waiting_for_payment_details)
async def handle_withdrawal_details(message: Message, state: FSMContext, session: AsyncSession):
    """Обработчик реквизитов для вывода"""
    payment_details = message.text
    
    data = await state.get_data()
    amount = data.get("withdrawal_amount")
    commission = data.get("commission")
    final_amount = data.get("final_amount")
    
    await state.update_data(payment_details=payment_details)
    
    text = f"""
💸 <b>Подтверждение вывода средств</b>

💰 Сумма: {amount} ₽
💸 Комиссия: {commission:.2f} ₽
✅ К получению: {final_amount:.2f} ₽

📋 Реквизиты: {payment_details}

⚠️ <b>Внимание:</b> Вывод средств обрабатывается в течение 24 часов в рабочие дни.
    """
    
    await message.answer(
        text,
        reply_markup=get_confirmation_keyboard("withdrawal")
    )


@router.callback_query(F.data == "confirm_withdrawal")
async def confirm_withdrawal(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Подтвердить вывод средств"""
    data = await state.get_data()
    
    payment_service = PaymentService(session)
    
    transaction = await payment_service.create_withdrawal_request(
        user_id=callback.from_user.id,
        amount=data.get("withdrawal_amount"),
        payment_details={
            "method": "bank_transfer",
            "details": data.get("payment_details")
        }
    )
    
    if transaction:
        await callback.message.edit_text(
            f"✅ <b>Заявка на вывод создана!</b>\n\n"
            f"🆔 ID заявки: {transaction.id}\n"
            f"💰 Сумма: {data.get('withdrawal_amount')} ₽\n"
            f"✅ К получению: {data.get('final_amount'):.2f} ₽\n\n"
            f"📋 Статус заявки можно отслеживать в разделе 'История транзакций'"
        )
    else:
        await callback.message.edit_text(
            "❌ <b>Ошибка при создании заявки</b>\n\n"
            "Попробуйте позже или обратитесь в поддержку."
        )
    
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_withdrawal")
async def cancel_withdrawal(callback: CallbackQuery, state: FSMContext):
    """Отменить вывод средств"""
    await state.clear()
    
    await callback.message.edit_text(
        "❌ <b>Вывод средств отменен</b>\n\n"
        "Вы можете создать новую заявку в любое время.",
        reply_markup=get_main_menu_keyboard()
    )
    
    await callback.answer()


@router.callback_query(F.data == "transaction_history")
async def show_transaction_history(callback: CallbackQuery, session: AsyncSession):
    """Показать историю транзакций"""
    user_service = UserService(session)
    user = await user_service.get_user_by_telegram_id(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Пользователь не найден")
        return
    
    transactions = await user_service.get_recent_transactions(user.id, limit=10)
    
    if not transactions:
        text = "📋 <b>История транзакций пуста</b>\n\nУ вас пока нет операций."
    else:
        text = "📋 <b>Последние транзакции:</b>\n\n"
        
        for transaction in transactions:
            status_emoji = "✅" if transaction.status.value == "completed" else "⏳"
            type_emoji = {
                "deposit": "💳",
                "withdrawal": "💸", 
                "tournament_fee": "🏆",
                "prize": "🎁",
                "referral_bonus": "🎁"
            }.get(transaction.transaction_type.value, "💰")
            
            text += f"{status_emoji} {type_emoji} {transaction.amount} ₽\n"
            text += f"   {transaction.description}\n"
            text += f"   {transaction.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu_keyboard()
    )
    
    await callback.answer()
