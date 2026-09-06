import sqlalchemy as sa
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Item
from utils.enums import ItemRarity


class ItemRepo:
    def session(self) -> AsyncContextManager[AsyncSession]:
        ...

    async def get_item(self, id: int) -> Item | None:
        stmt = sa.select(Item).where(Item.id == id)

        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_items(
        self,
        rarity: ItemRarity | None = None,
    ) -> list[Item]:
        stmt = sa.select(Item)
        if rarity is not None:
            stmt = stmt.where(Item.rarity == rarity)

        async with self.session() as session:
            result = await session.execute(stmt)
            return list(result.scalars().all())
