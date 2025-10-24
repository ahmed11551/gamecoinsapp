"""
Сервис для работы с пользователями
"""
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload

from app.database.models import User, Transaction, TransactionType, TransactionStatus


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID"""
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create_user(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        referrer_id: Optional[int] = None
    ) -> User:
        """Создать нового пользователя"""
        # Генерируем уникальный реферальный код
        referral_code = self._generate_referral_code()
        
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            referrer_id=referrer_id,
            referral_code=referral_code
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        # Если есть реферер, начисляем бонус
        if referrer_id:
            await self._process_referral_bonus(user.id, referrer_id)
        
        return user
    
    async def update_user_balance(self, user_id: int, amount: float) -> bool:
        """Обновить баланс пользователя"""
        try:
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(balance=User.balance + amount)
            )
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            return False
    
    async def add_transaction(
        self,
        user_id: int,
        amount: float,
        transaction_type: TransactionType,
        description: str,
        external_id: Optional[str] = None,
        payment_method: Optional[str] = None,
        tournament_id: Optional[int] = None
    ) -> Transaction:
        """Добавить транзакцию"""
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            external_id=external_id,
            payment_method=payment_method,
            tournament_id=tournament_id
        )
        
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        
        return transaction
    
    async def get_user_transactions(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Transaction]:
        """Получить транзакции пользователя"""
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
    
    async def get_recent_transactions(self, user_id: int, limit: int = 10) -> List[Transaction]:
        """Получить последние транзакции"""
        return await self.get_user_transactions(user_id, limit)
    
    async def update_user_stats(
        self,
        user_id: int,
        games_played: int = 0,
        games_won: int = 0,
        tournaments_played: int = 0,
        tournaments_won: int = 0,
        rating_change: int = 0
    ):
        """Обновить статистику пользователя"""
        await self.session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                games_played=User.games_played + games_played,
                games_won=User.games_won + games_won,
                tournaments_played=User.tournaments_played + tournaments_played,
                tournaments_won=User.tournaments_won + tournaments_won,
                rating=User.rating + rating_change,
                last_active=datetime.utcnow()
            )
        )
        await self.session.commit()
    
    async def verify_user(self, user_id: int) -> bool:
        """Верифицировать пользователя"""
        try:
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(is_verified=True)
            )
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False
    
    async def ban_user(self, user_id: int) -> bool:
        """Заблокировать пользователя"""
        try:
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(is_banned=True)
            )
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False
    
    async def unban_user(self, user_id: int) -> bool:
        """Разблокировать пользователя"""
        try:
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(is_banned=False)
            )
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False
    
    async def get_user_by_referral_code(self, referral_code: str) -> Optional[User]:
        """Получить пользователя по реферальному коду"""
        result = await self.session.execute(
            select(User).where(User.referral_code == referral_code)
        )
        return result.scalar_one_or_none()
    
    async def get_referrals(self, user_id: int) -> List[User]:
        """Получить рефералов пользователя"""
        result = await self.session.execute(
            select(User).where(User.referrer_id == user_id)
        )
        return result.scalars().all()
    
    async def get_top_users(self, limit: int = 10) -> List[User]:
        """Получить топ пользователей по рейтингу"""
        result = await self.session.execute(
            select(User)
            .where(User.is_banned == False)
            .order_by(User.rating.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_user_count(self) -> int:
        """Получить общее количество пользователей"""
        result = await self.session.execute(
            select(func.count(User.id))
        )
        return result.scalar()
    
    async def get_active_users_count(self, days: int = 7) -> int:
        """Получить количество активных пользователей за N дней"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(
            select(func.count(User.id))
            .where(User.last_active >= cutoff_date)
        )
        return result.scalar()
    
    def _generate_referral_code(self) -> str:
        """Генерировать уникальный реферальный код"""
        return ''.join(secrets.choices(string.ascii_uppercase + string.digits, k=8))
    
    async def _process_referral_bonus(self, new_user_id: int, referrer_id: int):
        """Обработать реферальный бонус"""
        # Бонус новому пользователю
        await self.add_transaction(
            user_id=new_user_id,
            amount=100.0,
            transaction_type=TransactionType.REFERRAL_BONUS,
            description="Бонус за регистрацию по реферальной ссылке"
        )
        
        # Бонус рефереру
        await self.add_transaction(
            user_id=referrer_id,
            amount=50.0,
            transaction_type=TransactionType.REFERRAL_BONUS,
            description="Бонус за приглашение друга"
        )
        
        # Обновляем балансы
        await self.update_user_balance(new_user_id, 100.0)
        await self.update_user_balance(referrer_id, 50.0)
