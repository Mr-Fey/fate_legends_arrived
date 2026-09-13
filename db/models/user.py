import sqlalchemy as sa 
from .base import BaseModel
from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING: 
    from .character_slot import CharacterSlot
    from .inventory_slot import InventorySlot


class User(BaseModel):   
    id: Mapped[int] = mapped_column(
        sa.BigInteger(),
        primary_key=True,
        autoincrement=False,
    )

    profile_data: Mapped[dict] = mapped_column(sa.JSON(), default={}, nullable=False)

    quartz: Mapped[float] = mapped_column(sa.Float(), default=0, nullable=False)
    negative_quartz: Mapped[float] = mapped_column(sa.Float(), default=0, nullable=False)
    gold_quartz: Mapped[float] = mapped_column(sa.Float(), default=0, nullable=False)

    characters: Mapped[List["CharacterSlot"]] = relationship(
        "CharacterSlot", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="selectin", 
    )
    inventory: Mapped[List["InventorySlot"]] = relationship(
        "InventorySlot", 
        back_populates="user", 
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property 
    def len_character_slots(self) -> int: 
        return len(self.characters)

    @property 
    def len_free_characters_slots(self) -> int: 
        return len(self.free_characters_slots)

    @property 
    def len_characters(self) -> int: 
        return len(self.characters_slots)

    @property 
    def characters_slots(self) -> List["CharacterSlot"]: 
        return [c for c in self.characters if c.character_id]
    
    @property
    def free_characters_slots(self) -> List["CharacterSlot"]: 
        return [c for c in self.characters if not c.character_id]
    
    @property
    def len_inventory_slots(self) -> int: 
        return len(self.inventory)
    
    @property 
    def len_free_inventory_slots(self) -> int: 
        return len([i for i in self.inventory if not i.item_id])

    @property 
    def len_inventory_items(self) -> int:
        return len(self.inventory_items) 
    
    @property 
    def inventory_items(self) -> List["InventorySlot"]: 
        return [i for i in self.inventory if i.item_id]
    
    @property 
    def free_inventory_slots(self) -> List["InventorySlot"]: 
        return [i for i in self.inventory if not i.item_id]
    
    @property
    def is_inkognito(self) -> bool: 
        return self.profile_data.get("inkognito", False)
    
    @property 
    def banner_id(self) -> int: 
        return self.profile_data.get("banner_id", 1)
