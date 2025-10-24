"""
Сервис для работы с платежами
"""
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.database.models import User, Transaction, TransactionType, TransactionStatus
from app.config import settings


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_deposit_request(
        self,
        user_id: int,
        amount: float,
        payment_method: str
    ) -> Transaction:
        """Создать запрос на пополнение"""
        transaction = await self.session.execute(
            select(Transaction)
            .where(
                Transaction.user_id == user_id,
                Transaction.transaction_type == TransactionType.DEPOSIT,
                Transaction.status == TransactionStatus.PENDING
            )
        )
        existing_transaction = transaction.scalar_one_or_none()
        
        if existing_transaction:
            return existing_transaction
        
        new_transaction = Transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            description=f"Пополнение через {payment_method}",
            payment_method=payment_method,
            status=TransactionStatus.PENDING
        )
        
        self.session.add(new_transaction)
        await self.session.commit()
        await self.session.refresh(new_transaction)
        
        return new_transaction
    
    async def process_telegram_stars_payment(
        self,
        user_id: int,
        amount: float,
        external_id: str
    ) -> bool:
        """Обработать платеж через Telegram Stars"""
        try:
            # Находим транзакцию
            result = await self.session.execute(
                select(Transaction)
                .where(
                    Transaction.user_id == user_id,
                    Transaction.transaction_type == TransactionType.DEPOSIT,
                    Transaction.status == TransactionStatus.PENDING
                )
                .order_by(Transaction.created_at.desc())
            )
            transaction = result.scalar_one_or_none()
            
            if not transaction:
                return False
            
            # Обновляем транзакцию
            await self.session.execute(
                update(Transaction)
                .where(Transaction.id == transaction.id)
                .values(
                    status=TransactionStatus.COMPLETED,
                    external_id=external_id,
                    processed_at=datetime.utcnow()
                )
            )
            
            # Обновляем баланс пользователя
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    balance=User.balance + amount,
                    total_deposits=User.total_deposits + amount
                )
            )
            
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            return False
    
    async def create_withdrawal_request(
        self,
        user_id: int,
        amount: float,
        payment_details: Dict[str, Any]
    ) -> Optional[Transaction]:
        """Создать запрос на вывод средств"""
        # Проверяем минимальную сумму
        if amount < settings.MIN_WITHDRAWAL_AMOUNT:
            return None
        
        # Проверяем баланс
        user_result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user or user.balance < amount:
            return None
        
        # Рассчитываем комиссию
        commission = amount * settings.WITHDRAWAL_COMMISSION
        final_amount = amount - commission
        
        transaction = Transaction(
            user_id=user_id,
            amount=final_amount,
            transaction_type=TransactionType.WITHDRAWAL,
            description=f"Вывод средств. Комиссия: {commission:.2f} ₽",
            payment_method=payment_details.get("method", "unknown"),
            status=TransactionStatus.PENDING
        )
        
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        
        return transaction
    
    async def process_withdrawal(
        self,
        transaction_id: int,
        external_id: Optional[str] = None
    ) -> bool:
        """Обработать вывод средств"""
        try:
            # Находим транзакцию
            result = await self.session.execute(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            transaction = result.scalar_one_or_none()
            
            if not transaction or transaction.status != TransactionStatus.PENDING:
                return False
            
            # Обновляем транзакцию
            await self.session.execute(
                update(Transaction)
                .where(Transaction.id == transaction_id)
                .values(
                    status=TransactionStatus.COMPLETED,
                    external_id=external_id,
                    processed_at=datetime.utcnow()
                )
            )
            
            # Обновляем баланс пользователя
            await self.session.execute(
                update(User)
                .where(User.id == transaction.user_id)
                .values(
                    balance=User.balance - transaction.amount,
                    total_withdrawals=User.total_withdrawals + transaction.amount
                )
            )
            
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            return False
    
    async def calculate_commission(self, amount: float) -> float:
        """Рассчитать комиссию платформы"""
        if amount < 500:
            return amount * settings.COMMISSION_RATES["low"]
        elif amount < 2000:
            return amount * settings.COMMISSION_RATES["medium"]
        else:
            return amount * settings.COMMISSION_RATES["high"]
    
    async def process_tournament_payment(
        self,
        user_id: int,
        tournament_id: int,
        entry_fee: float
    ) -> bool:
        """Обработать платеж за участие в турнире"""
        try:
            # Проверяем баланс
            user_result = await self.session.execute(
                select(User).where(User.id == user_id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user or user.balance < entry_fee:
                return False
            
            # Создаем транзакцию
            transaction = Transaction(
                user_id=user_id,
                amount=entry_fee,
                transaction_type=TransactionType.TOURNAMENT_FEE,
                description=f"Взнос за участие в турнире #{tournament_id}",
                tournament_id=tournament_id,
                status=TransactionStatus.COMPLETED,
                processed_at=datetime.utcnow()
            )
            
            self.session.add(transaction)
            
            # Обновляем баланс
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(balance=User.balance - entry_fee)
            )
            
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            return False
    
    async def process_prize_payment(
        self,
        user_id: int,
        tournament_id: int,
        prize_amount: float
    ) -> bool:
        """Обработать выплату приза"""
        try:
            # Создаем транзакцию
            transaction = Transaction(
                user_id=user_id,
                amount=prize_amount,
                transaction_type=TransactionType.PRIZE,
                description=f"Приз за турнир #{tournament_id}",
                tournament_id=tournament_id,
                status=TransactionStatus.COMPLETED,
                processed_at=datetime.utcnow()
            )
            
            self.session.add(transaction)
            
            # Обновляем баланс и статистику
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(
                    balance=User.balance + prize_amount,
                    total_winnings=User.total_winnings + prize_amount
                )
            )
            
            await self.session.commit()
            return True
            
        except Exception as e:
            await self.session.rollback()
            return False
    
    async def get_pending_withdrawals(self) -> list[Transaction]:
        """Получить ожидающие выводы"""
        result = await self.session.execute(
            select(Transaction)
            .where(
                Transaction.transaction_type == TransactionType.WITHDRAWAL,
                Transaction.status == TransactionStatus.PENDING
            )
            .order_by(Transaction.created_at.asc())
        )
        return result.scalars().all()
    
    async def cancel_transaction(self, transaction_id: int) -> bool:
        """Отменить транзакцию"""
        try:
            await self.session.execute(
                update(Transaction)
                .where(Transaction.id == transaction_id)
                .values(
                    status=TransactionStatus.CANCELLED,
                    processed_at=datetime.utcnow()
                )
            )
            await self.session.commit()
            return True
        except Exception:
            await self.session.rollback()
            return False
