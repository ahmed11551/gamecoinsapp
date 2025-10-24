"""
Пример конфигурации для разработки
"""
import os
from app.config import Settings

# Пример настроек для локальной разработки
DEV_CONFIG = {
    "BOT_TOKEN": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
    "WEBHOOK_URL": None,  # Для polling режима
    "WEBHOOK_PATH": "/webhook",
    
    "DATABASE_URL": "postgresql://postgres:password@localhost:5432/tournament_bot_dev",
    "REDIS_URL": "redis://localhost:6379/0",
    
    "TELEGRAM_STARS_API_KEY": None,  # Получить от Telegram
    "YOO_KASSA_SHOP_ID": None,       # Получить от ЮKassa
    "YOO_KASSA_SECRET_KEY": None,    # Получить от ЮKassa
    "BINANCE_API_KEY": None,         # Получить от Binance
    
    "SECRET_KEY": "dev-secret-key-change-in-production",
    "ADMIN_USER_IDS": [123456789],   # Ваш Telegram ID
    
    "MIN_WITHDRAWAL_AMOUNT": 500.0,
    "WITHDRAWAL_COMMISSION": 0.03,
    "RESERVE_PERCENTAGE": 0.05,
    
    "COMMISSION_RATES": {
        "low": 0.20,    # До 500 ₽
        "medium": 0.15, # 500-2000 ₽
        "high": 0.10    # От 2000 ₽
    },
    
    "DUEL_TIMEOUT": 1800,      # 30 минут
    "GROUP_TOURNAMENT_TIMEOUT": 3600,  # 1 час
    "MARATHON_TIMEOUT": 86400,  # 24 часа
}

# Создание .env файла для разработки
def create_dev_env():
    """Создать .env файл для разработки"""
    env_content = "\n".join([f"{key}={value}" for key, value in DEV_CONFIG.items()])
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ Создан .env файл для разработки")
    print("📝 Отредактируйте файл и добавьте реальные токены")

if __name__ == "__main__":
    create_dev_env()
