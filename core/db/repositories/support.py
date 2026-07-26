from datetime import datetime

from sqlalchemy import select, func

from core.db.models import SupportTicket, TicketStatus
from core.db.repositories.base import BaseRepository


class SupportTicketRepository(BaseRepository[SupportTicket]):
    model = SupportTicket

    async def get_open_by_user(self, user_id: int) -> SupportTicket | None:
        result = await self.session.execute(
            select(SupportTicket).where(
                SupportTicket.user_id == user_id,
                SupportTicket.status != TicketStatus.CLOSED,
                ).limit(1)
        )
        return result.scalar_one_or_none()

    async def count_today_by_user(self, user_id: int) -> int:
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result = await self.session.execute(
            select(func.count()).select_from(SupportTicket).where(
                SupportTicket.user_id == user_id,
                SupportTicket.created_at >= today_start,
            )
        )
        return result.scalar_one()
