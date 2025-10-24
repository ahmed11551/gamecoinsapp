"""
Конфигурация приложения
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Telegram Bot
    BOT_TOKEN: str
    WEBHOOK_URL: Optional[str] = None
    WEBHOOK_PATH: str = "/webhook"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/tournament_bot"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Payment Systems
    TELEGRAM_STARS_API_KEY: Optional[str] = None
    YOO_KASSA_SHOP_ID: Optional[str] = None
    YOO_KASSA_SECRET_KEY: Optional[str] = None
    BINANCE_API_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ADMIN_USER_IDS: list[int] = []
    
    # Tournament Settings
    MIN_WITHDRAWAL_AMOUNT: float = 500.0  # ₽
    WITHDRAWAL_COMMISSION: float = 0.03   # 3%
    RESERVE_PERCENTAGE: float = 0.05      # 5%
    
    # Commission Rates
    COMMISSION_RATES: dict = {
        "low": 0.20,    # До 500 ₽
        "medium": 0.15, # 500-2000 ₽
        "high": 0.10    # От 2000 ₽
    }
    
    # Game Settings
    DUEL_TIMEOUT: int = 1800  # 30 минут
    GROUP_TOURNAMENT_TIMEOUT: int = 3600  # 1 час
    MARATHON_TIMEOUT: int = 86400  # 24 часа
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Глобальный экземпляр настроек
settings = Settings()
