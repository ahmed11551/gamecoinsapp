"""
Состояния FSM для бота
"""
from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    waiting_for_phone = State()
    waiting_for_verification = State()


class TournamentCreation(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_entry_fee = State()
    waiting_for_max_participants = State()
    waiting_for_confirmation = State()


class PaymentStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_payment_method = State()
    waiting_for_confirmation = State()


class WithdrawalStates(StatesGroup):
    waiting_for_amount = State()
    waiting_for_payment_details = State()
    waiting_for_confirmation = State()


class GameStates(StatesGroup):
    playing_game = State()
    submitting_score = State()
    waiting_for_opponent = State()
