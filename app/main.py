"""
Основной файл бота
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.config import settings
from app.database.connection import db
from app.bot.handlers import register_handlers
from app.bot.middlewares import register_middlewares

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """Инициализация при запуске"""
    logger.info("Starting bot...")
    
    # Создание таблиц базы данных
    await db.create_tables()
    logger.info("Database tables created")
    
    # Установка webhook (если используется)
    if settings.WEBHOOK_URL:
        webhook_url = f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    else:
        # Удаление webhook для polling режима
        await bot.delete_webhook()
        logger.info("Webhook deleted, using polling mode")


async def on_shutdown(bot: Bot):
    """Очистка при завершении"""
    logger.info("Shutting down bot...")
    await bot.delete_webhook()


def create_bot() -> Bot:
    """Создание экземпляра бота"""
    return Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


def create_dispatcher() -> Dispatcher:
    """Создание диспетчера"""
    dp = Dispatcher()
    
    # Регистрация middleware
    register_middlewares(dp)
    
    # Регистрация обработчиков
    register_handlers(dp)
    
    return dp


async def create_app() -> web.Application:
    """Создание веб-приложения для webhook"""
    bot = create_bot()
    dp = create_dispatcher()
    
    # Обработчики событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Создание веб-приложения
    app = web.Application()
    
    # Настройка webhook
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)
    
    setup_application(app, dp, bot=bot)
    
    return app


async def main():
    """Основная функция для запуска бота"""
    bot = create_bot()
    dp = create_dispatcher()
    
    # Обработчики событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        # Запуск бота
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
