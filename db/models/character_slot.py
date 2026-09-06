import sqlalchemy as sa 
from .base import BaseModel
from utils.enums import CharacterRarity
from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING: 
    from .user import User 
    from .character import Character


class CharacterSlot(BaseModel): 
    __table_args__ = (
        sa.UniqueConstraint("user_id", "index", name="uq_user_slot_index"),
    )

    id: Mapped[int] = mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )
    index: Mapped[int] = mapped_column(sa.Integer(), nullable=False)  # номер слота
    image_url: Mapped[Optional[str]] = mapped_column(sa.Text(), nullable=True) #banner

    character_id: Mapped[Optional[int]] = mapped_column(
        sa.ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="characters",
        lazy="selectin",
    )
    character: Mapped["Character"] = relationship(
        "Character",
        lazy="joined",
    )

    @property
    def name(self) -> str: 
        return self.character.name
    
    @property 
    def rarity(self) -> CharacterRarity: 
        return self.character.rarity 
    
    @property 
    def description(self) -> str: 
        return self.character.description
    
    @property 
    def full_description(self) -> str: 
        return self.character.full_description

    @property 
    def icon(self) -> str: 
        return self.character.icon

    @property 
    def character_rating(self) -> float: 
        return self.character.character_rating
        
    @property 
    def price(self) -> float: 
        return self.character.price