"""
Модели базы данных
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    BigInteger, Boolean, Column, DateTime, ForeignKey, 
    Integer, Numeric, String, Text, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum

Base = declarative_base()


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TOURNAMENT_FEE = "tournament_fee"
    PRIZE = "prize"
    REFERRAL_BONUS = "referral_bonus"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TournamentType(str, Enum):
    DUEL = "duel"
    GROUP = "group"
    MARATHON = "marathon"


class TournamentStatus(str, Enum):
    CREATED = "created"
    REGISTRATION = "registration"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GameType(str, Enum):
    CLICKER = "clicker"
    REACTION = "reaction"
    GAME_2048 = "2048"
    CHESS = "chess"
    BACKGAMMON = "backgammon"
    CHECKERS = "checkers"
    TETRIS = "tetris"
    MINESWEEPER = "minesweeper"
    SHOOTING_GALLERY = "shooting_gallery"


class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(32), nullable=True)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    
    # Финансы
    balance = Column(Numeric(10, 2), default=0, nullable=False)
    total_deposits = Column(Numeric(10, 2), default=0, nullable=False)
    total_withdrawals = Column(Numeric(10, 2), default=0, nullable=False)
    total_winnings = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Статистика
    rating = Column(Integer, default=1000, nullable=False)
    games_played = Column(Integer, default=0, nullable=False)
    games_won = Column(Integer, default=0, nullable=False)
    tournaments_played = Column(Integer, default=0, nullable=False)
    tournaments_won = Column(Integer, default=0, nullable=False)
    
    # Статус
    is_verified = Column(Boolean, default=False, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False)
    
    # Реферальная система
    referrer_id = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    referral_code = Column(String(16), unique=True, nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_active = Column(DateTime, default=datetime.utcnow, nullable=False)
    premium_until = Column(DateTime, nullable=True)
    
    # Связи
    transactions = relationship("Transaction", back_populates="user")
    tournaments_as_participant = relationship("Participant", back_populates="user")
    tournaments_as_creator = relationship("Tournament", back_populates="creator")
    referrals = relationship("User", back_populates="referrer")
    referrer = relationship("User", back_populates="referrals", remote_side=[id])


class Tournament(Base):
    __tablename__ = "tournaments"
    
    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    # Основная информация
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    game_type = Column(SQLEnum(GameType), nullable=False)
    tournament_type = Column(SQLEnum(TournamentType), nullable=False)
    
    # Финансы
    entry_fee = Column(Numeric(10, 2), nullable=False)
    prize_pool = Column(Numeric(10, 2), default=0, nullable=False)
    platform_commission = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Настройки
    max_participants = Column(Integer, nullable=False)
    min_participants = Column(Integer, default=2, nullable=False)
    prize_distribution = Column(Text, nullable=True)  # JSON строка
    
    # Статус
    status = Column(SQLEnum(TournamentStatus), default=TournamentStatus.CREATED, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    registration_ends_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    
    # Связи
    creator = relationship("User", back_populates="tournaments_as_creator")
    participants = relationship("Participant", back_populates="tournament")


class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    tournament_id = Column(BigInteger, ForeignKey("tournaments.id"), nullable=False)
    
    # Результаты
    final_position = Column(Integer, nullable=True)
    score = Column(Numeric(10, 2), nullable=True)
    winnings = Column(Numeric(10, 2), default=0, nullable=False)
    
    # Статус участия
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime, nullable=True)
    
    # Связи
    user = relationship("User", back_populates="tournaments_as_participant")
    tournament = relationship("Tournament", back_populates="participants")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    # Основная информация
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    
    # Дополнительная информация
    description = Column(Text, nullable=True)
    external_id = Column(String(128), nullable=True)  # ID в платежной системе
    payment_method = Column(String(32), nullable=True)  # telegram_stars, yookassa, crypto
    
    # Связанные объекты
    tournament_id = Column(BigInteger, ForeignKey("tournaments.id"), nullable=True)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    # Связи
    user = relationship("User", back_populates="transactions")
    tournament = relationship("Tournament")


class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(BigInteger, primary_key=True)
    tournament_id = Column(BigInteger, ForeignKey("tournaments.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    # Игровые данные
    game_type = Column(SQLEnum(GameType), nullable=False)
    game_data = Column(Text, nullable=True)  # JSON с игровыми данными
    score = Column(Numeric(10, 2), nullable=True)
    
    # Статус
    is_completed = Column(Boolean, default=False, nullable=False)
    is_validated = Column(Boolean, default=False, nullable=False)
    
    # Временные метки
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Связи
    tournament = relationship("Tournament")
    user = relationship("User")


class ReserveFund(Base):
    __tablename__ = "reserve_fund"
    
    id = Column(BigInteger, primary_key=True)
    balance = Column(Numeric(10, 2), default=0, nullable=False)
    total_contributions = Column(Numeric(10, 2), default=0, nullable=False)
    total_payouts = Column(Numeric(10, 2), default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ReferralBonus(Base):
    __tablename__ = "referral_bonuses"
    
    id = Column(BigInteger, primary_key=True)
    referrer_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    referred_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    
    bonus_amount = Column(Numeric(10, 2), nullable=False)
    commission_rate = Column(Numeric(5, 4), nullable=False)  # 0.1000 = 10%
    total_commission = Column(Numeric(10, 2), default=0, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Связи
    referrer = relationship("User", foreign_keys=[referrer_id])
    referred = relationship("User", foreign_keys=[referred_id])
