import sqlalchemy as sa
from datetime import datetime
from typing import AsyncContextManager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from settings import conf
from db.models import CharacterSlot, InventorySlot, Item, User


class UserRepo:
    def session(self) -> AsyncContextManager[AsyncSession]:
        ...

    async def create_user(
        self,
        id: int,
        **kwargs
    ) -> User:
        user = User(id=id, **kwargs)
        user.characters = [CharacterSlot(index=i) for i in range(3)]
        user.inventory = [InventorySlot(index=i) for i in range(10)]

        async with self.session() as session:
            session.add(user)
            await session.flush()
            await session.commit()
        return user

    async def get_user(self, id: int) -> User | None:
        stmt = sa.select(User).where(User.id == id)

        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_users(self) -> list[User]:
        stmt = (
            sa.select(User)
            .options(
                selectinload(User.characters).joinedload(CharacterSlot.character),
            )
        )
        async with self.session() as session:
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def create_or_get_user(
        self,
        id: int,
        **kwargs, 
    ) -> User:
        user = await self.get_user(id=id)
        if user is None:
            user = await self.create_user(id=id, **kwargs)
        return user

    async def update_user_character_slot(
        self,
        user_id: int,
        slot_index: int,
        **kwargs,
    ) -> None:
        stmt = (
            sa.update(CharacterSlot)
            .where(
                CharacterSlot.user_id == user_id,
                CharacterSlot.index == slot_index,
            )
            .values(**kwargs)
        )
        async with self.session() as session:
            await session.execute(stmt)
            await session.commit()

    async def update_user_item_slot(
        self,
        user_id: int,
        slot_index: int,
        **kwargs,
    ) -> None:
        stmt = (
            sa.update(InventorySlot)
            .where(
                InventorySlot.user_id == user_id,
                InventorySlot.index == slot_index,
            )
            .values(**kwargs)
        )
        async with self.session() as session:
            await session.execute(stmt)
            await session.commit()

    async def user_use_item(
        self, 
        user_id: int, 
        slot: InventorySlot, 
    ) -> None: 
        if slot.item_id is None: return 
        if slot.quantity <= 1: 
            await self.update_user_item_slot(
                user_id=user_id, 
                slot_index=slot.index, 
                item_id=None, 
                quantity=0, 
            )
        else: 
            await self.update_user_item_slot(
                user_id=user_id, 
                slot_index=slot.index, 
                quantity=slot.quantity - 1, 
            )
    
    async def user_drop_item(
        self, 
        user_id: int, 
        slot: InventorySlot, 
        amount: int, 
    ) -> None: 
        if slot.item_id is None: return 
        if slot.quantity <= amount: 
            await self.update_user_item_slot(
                user_id=user_id, 
                slot_index=slot.index, 
                item_id=None, 
                quantity=0, 
            )
        else: 
            await self.update_user_item_slot(
                user_id=user_id, 
                slot_index=slot.index, 
                quantity=slot.quantity - amount, 
            )

    async def update_user_money(
        self,
        user_id: int,
        type: str, 
        delta: float,
    ) -> None:
        quartz_field = conf.quartz_types.get(type, "quartz")
        update_values = {quartz_field: getattr(User, quartz_field) + delta}

        stmt = (
            sa.update(User)
            .where(User.id == user_id)
            .values(**update_values)
        )

        async with self.session() as session:
                await session.execute(stmt)
                await session.commit()

    async def update_user_profile_data(
        self,
        user_id: int,
        **kwargs,
    ) -> User | None:
        user = await self.get_user(id=user_id)
        if user is None:
            return None

        profile_data = dict(user.profile_data or {})
        profile_data.update(kwargs)

        stmt = (
            sa.update(User)
            .where(User.id == user_id)
            .values(profile_data=profile_data)
        )

        async with self.session() as session:
            await session.execute(stmt)
            await session.commit()
        return await self.get_user(id=user_id)

    async def add_item_to_inventory(
        self,
        user_id: int,
        item_id: int,
        quantity: int = 1,
    ) -> bool:
        user = await self.create_or_get_user(id=user_id)
        if user is None:
            return False

        item_stmt = sa.select(Item).where(Item.id == item_id)
        async with self.session() as session:
            item_result = await session.execute(item_stmt)
            item = item_result.scalar_one_or_none()
            if item is None:
                return False

        free_slots = sorted(
            user.free_inventory_slots,
            key=lambda slot: slot.index,
        )

        stack_limit = max(item.stack_limit, 1)
        remaining = quantity

        if stack_limit > 1:
            existing_slots = sorted(
                [slot for slot in user.inventory_items if slot.item_id == item.id],
                key=lambda slot: slot.index,
            )

            for slot in existing_slots:
                current_quantity = slot.quantity or 0
                if current_quantity >= stack_limit:
                    continue

                add_quantity = min(stack_limit - current_quantity, remaining)
                new_quantity = current_quantity + add_quantity

                await self.update_user_item_slot(
                    user_id=user_id,
                    slot_index=slot.index,
                    quantity=new_quantity,
                )
                remaining -= add_quantity

                if remaining <= 0:
                    return True

        while remaining > 0:
            if not free_slots:
                return False  

            slot = free_slots.pop(0)
            add_quantity = 1 if stack_limit == 1 else min(remaining, stack_limit)

            await self.update_user_item_slot(
                user_id=user_id,
                slot_index=slot.index,
                item_id=item.id,
                quantity=add_quantity,
            )
            remaining -= add_quantity

        return True
