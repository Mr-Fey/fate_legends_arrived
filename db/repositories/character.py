import sqlalchemy as sa
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Character
from utils.enums import CharacterRarity


class CharacterRepo:
    def session(self) -> AsyncContextManager[AsyncSession]:
        ...

    async def create_character(self, **kwargs) -> None: 
        async with self.session() as session: 
            character = Character(**kwargs)
            session.add(character) 
            await session.flush()
            await session.commit()

    async def get_all_characters(
        self,
        rarity: CharacterRarity | None = None,
    ) -> list[Character]:
        stmt = sa.select(Character)
        if rarity is not None:
            stmt = stmt.where(Character.rarity == rarity)
        async with self.session() as session:
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def get_character_by_name(self, name: str) -> Character | None:
        stmt = sa.select(Character).where(sa.func.lower(Character.name) == name.lower())

        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


    async def get_character_by_id(self, id: int) -> Character | None:
        stmt = sa.select(Character).where(Character.id == id)

        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    
