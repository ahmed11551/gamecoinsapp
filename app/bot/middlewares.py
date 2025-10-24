"""
Middleware для бота
"""
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import db
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    """Middleware для работы с базой данных"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with db.async_session() as session:
            data["session"] = session
            return await handler(event, data)


class UserMiddleware(BaseMiddleware):
    """Middleware для работы с пользователями"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data.get("session")
        
        if session and hasattr(event, "from_user") and event.from_user:
            user_service = UserService(session)
            user = await user_service.get_user_by_telegram_id(event.from_user.id)
            data["user"] = user
        
        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if hasattr(event, "from_user") and event.from_user:
            logger.info(
                f"User {event.from_user.id} ({event.from_user.username}) "
                f"triggered {type(event).__name__}"
            )
        
        return await handler(event, data)


def register_middlewares(dp):
    """Регистрация всех middleware"""
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())
    
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
