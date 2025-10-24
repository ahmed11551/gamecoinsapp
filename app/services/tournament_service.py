"""
Сервис для работы с турнирами
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload

from app.database.models import (
    Tournament, Participant, User, TournamentType, 
    TournamentStatus, GameType, Transaction, TransactionType
)
from app.services.payment_service import PaymentService
from app.services.user_service import UserService


class TournamentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.payment_service = PaymentService(session)
        self.user_service = UserService(session)
    
    async def create_tournament(
        self,
        creator_id: int,
        title: str,
        description: str,
        game_type: GameType,
        tournament_type: TournamentType,
        entry_fee: float,
        max_participants: int,
        min_participants: int = 2
    ) -> Tournament:
        """Создать новый турнир"""
        # Рассчитываем комиссию платформы
        commission_rate = await self._get_commission_rate(entry_fee)
        platform_commission = entry_fee * commission_rate
        
        # Рассчитываем призовой фонд
        prize_pool = entry_fee * max_participants * (1 - commission_rate)
        
        # Определяем распределение призов
        prize_distribution = self._get_prize_distribution(tournament_type)
        
        tournament = Tournament(
            creator_id=creator_id,
            title=title,
            description=description,
            game_type=game_type,
            tournament_type=tournament_type,
            entry_fee=entry_fee,
            prize_pool=prize_pool,
            platform_commission=platform_commission,
            max_participants=max_participants,
            min_participants=min_participants,
            prize_distribution=prize_distribution,
            status=TournamentStatus.CREATED
        )
        
        self.session.add(tournament)
        await self.session.commit()
        await self.session.refresh(tournament)
        
        return tournament
    
    async def join_tournament(self, tournament_id: int, user_id: int) -> bool:
        """Участвовать в турнире"""
        # Получаем турнир
        result = await self.session.execute(
            select(Tournament)
            .where(Tournament.id == tournament_id)
            .options(selectinload(Tournament.participants))
        )
        tournament = result.scalar_one_or_none()
        
        if not tournament:
            return False
        
        # Проверяем статус турнира
        if tournament.status != TournamentStatus.REGISTRATION:
            return False
        
        # Проверяем количество участников
        if len(tournament.participants) >= tournament.max_participants:
            return False
        
        # Проверяем, не участвует ли уже пользователь
        existing_participant = await self.session.execute(
            select(Participant)
            .where(
                Participant.tournament_id == tournament_id,
                Participant.user_id == user_id
            )
        )
        if existing_participant.scalar_one_or_none():
            return False
        
        # Обрабатываем платеж
        payment_success = await self.payment_service.process_tournament_payment(
            user_id=user_id,
            tournament_id=tournament_id,
            entry_fee=tournament.entry_fee
        )
        
        if not payment_success:
            return False
        
        # Добавляем участника
        participant = Participant(
            user_id=user_id,
            tournament_id=tournament_id
        )
        
        self.session.add(participant)
        await self.session.commit()
        
        # Проверяем, можно ли начать турнир
        await self._check_tournament_ready(tournament_id)
        
        return True
    
    async def start_tournament(self, tournament_id: int) -> bool:
        """Начать турнир"""
        result = await self.session.execute(
            select(Tournament)
            .where(Tournament.id == tournament_id)
            .options(selectinload(Tournament.participants))
        )
        tournament = result.scalar_one_or_none()
        
        if not tournament:
            return False
        
        # Проверяем минимальное количество участников
        if len(tournament.participants) < tournament.min_participants:
            return False
        
        # Обновляем статус турнира
        await self.session.execute(
            update(Tournament)
            .where(Tournament.id == tournament_id)
            .values(
                status=TournamentStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            )
        )
        
        await self.session.commit()
        
        # Запускаем турнир
        await self._run_tournament(tournament_id)
        
        return True
    
    async def submit_game_result(
        self,
        tournament_id: int,
        user_id: int,
        score: float,
        game_data: Dict[str, Any]
    ) -> bool:
        """Отправить результат игры"""
        # Находим участника
        result = await self.session.execute(
            select(Participant)
            .where(
                Participant.tournament_id == tournament_id,
                Participant.user_id == user_id
            )
        )
        participant = result.scalar_one_or_none()
        
        if not participant:
            return False
        
        # Обновляем результат
        await self.session.execute(
            update(Participant)
            .where(Participant.id == participant.id)
            .values(score=score)
        )
        
        await self.session.commit()
        
        # Проверяем, завершен ли турнир
        await self._check_tournament_completion(tournament_id)
        
        return True
    
    async def get_active_tournaments(self, game_type: Optional[GameType] = None) -> List[Tournament]:
        """Получить активные турниры"""
        query = select(Tournament).where(
            Tournament.status.in_([
                TournamentStatus.REGISTRATION,
                TournamentStatus.IN_PROGRESS
            ])
        )
        
        if game_type:
            query = query.where(Tournament.game_type == game_type)
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_tournament_by_id(self, tournament_id: int) -> Optional[Tournament]:
        """Получить турнир по ID"""
        result = await self.session.execute(
            select(Tournament)
            .where(Tournament.id == tournament_id)
            .options(selectinload(Tournament.participants))
        )
        return result.scalar_one_or_none()
    
    async def get_user_tournaments(self, user_id: int, limit: int = 20) -> List[Tournament]:
        """Получить турниры пользователя"""
        result = await self.session.execute(
            select(Tournament)
            .join(Participant)
            .where(Participant.user_id == user_id)
            .order_by(Tournament.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def _get_commission_rate(self, entry_fee: float) -> float:
        """Получить ставку комиссии"""
        if entry_fee < 500:
            return 0.20  # 20%
        elif entry_fee < 2000:
            return 0.15  # 15%
        else:
            return 0.10  # 10%
    
    def _get_prize_distribution(self, tournament_type: TournamentType) -> str:
        """Получить распределение призов"""
        if tournament_type == TournamentType.DUEL:
            return '{"1": 0.9}'  # 90% победителю
        elif tournament_type == TournamentType.GROUP:
            return '{"1": 0.5, "2": 0.3, "3": 0.2}'  # 50%, 30%, 20%
        else:  # MARATHON
            return '{"1": 0.4, "2": 0.25, "3": 0.15, "4-10": 0.2}'  # 40%, 25%, 15%, 20%
    
    async def _check_tournament_ready(self, tournament_id: int):
        """Проверить, готов ли турнир к запуску"""
        tournament = await self.get_tournament_by_id(tournament_id)
        
        if not tournament:
            return
        
        # Если набралось достаточно участников, начинаем турнир
        if len(tournament.participants) >= tournament.min_participants:
            await self.start_tournament(tournament_id)
    
    async def _run_tournament(self, tournament_id: int):
        """Запустить турнир"""
        tournament = await self.get_tournament_by_id(tournament_id)
        
        if not tournament:
            return
        
        if tournament.tournament_type == TournamentType.DUEL:
            await self._run_duel_tournament(tournament)
        elif tournament.tournament_type == TournamentType.GROUP:
            await self._run_group_tournament(tournament)
        else:  # MARATHON
            await self._run_marathon_tournament(tournament)
    
    async def _run_duel_tournament(self, tournament: Tournament):
        """Запустить дуэльный турнир"""
        participants = tournament.participants
        
        if len(participants) != 2:
            return
        
        # Для дуэли просто ждем результатов от обоих участников
        # Турнир завершится автоматически при получении всех результатов
        pass
    
    async def _run_group_tournament(self, tournament: Tournament):
        """Запустить групповой турнир"""
        # Для группового турнира создаем турнирную сетку
        # Пока что просто ждем результатов от всех участников
        pass
    
    async def _run_marathon_tournament(self, tournament: Tournament):
        """Запустить марафонский турнир"""
        # Марафонский турнир длится 24 часа
        # Участники могут играть несколько раз, засчитывается лучший результат
        pass
    
    async def _check_tournament_completion(self, tournament_id: int):
        """Проверить завершение турнира"""
        tournament = await self.get_tournament_by_id(tournament_id)
        
        if not tournament:
            return
        
        # Проверяем, все ли участники отправили результаты
        participants_with_scores = await self.session.execute(
            select(Participant)
            .where(
                Participant.tournament_id == tournament_id,
                Participant.score.isnot(None)
            )
        )
        
        participants_with_scores = participants_with_scores.scalars().all()
        
        if len(participants_with_scores) == len(tournament.participants):
            await self._complete_tournament(tournament_id)
    
    async def _complete_tournament(self, tournament_id: int):
        """Завершить турнир и распределить призы"""
        tournament = await self.get_tournament_by_id(tournament_id)
        
        if not tournament:
            return
        
        # Получаем участников с результатами
        participants = await self.session.execute(
            select(Participant)
            .where(Participant.tournament_id == tournament_id)
            .order_by(Participant.score.desc())
        )
        participants = participants.scalars().all()
        
        # Определяем победителей
        import json
        prize_distribution = json.loads(tournament.prize_distribution)
        
        for i, participant in enumerate(participants):
            position = i + 1
            
            # Определяем размер приза
            prize_percentage = 0
            for pos_range, percentage in prize_distribution.items():
                if pos_range == str(position):
                    prize_percentage = percentage
                    break
                elif "-" in pos_range:
                    start, end = map(int, pos_range.split("-"))
                    if start <= position <= end:
                        prize_percentage = percentage
                        break
            
            if prize_percentage > 0:
                prize_amount = tournament.prize_pool * prize_percentage
                
                # Обновляем позицию и выигрыш
                await self.session.execute(
                    update(Participant)
                    .where(Participant.id == participant.id)
                    .values(
                        final_position=position,
                        winnings=prize_amount
                    )
                )
                
                # Выплачиваем приз
                await self.payment_service.process_prize_payment(
                    user_id=participant.user_id,
                    tournament_id=tournament_id,
                    prize_amount=prize_amount
                )
        
        # Обновляем статус турнира
        await self.session.execute(
            update(Tournament)
            .where(Tournament.id == tournament_id)
            .values(
                status=TournamentStatus.COMPLETED,
                ended_at=datetime.utcnow()
            )
        )
        
        await self.session.commit()
