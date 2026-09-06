import sqlalchemy as sa 
from .base import BaseModel

from typing import List, Optional
from math import sqrt, log10

from settings import conf
from utils.enums import CharacterRarity
from utils.economy import normalize_value
from sqlalchemy.orm import Mapped, mapped_column



class Character(BaseModel): 
    id: Mapped[int] = mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(sa.String(32), unique=True, nullable=False)

    description: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    full_description: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    
    banners: Mapped[List[str]] = mapped_column(sa.JSON(), nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(sa.Text(), nullable=True) #TODO Покачто не у всех есть иконка

    rarity: Mapped[CharacterRarity] = mapped_column(sa.Enum(CharacterRarity))
    chance: Mapped[float] = mapped_column(sa.Float())

    @property 
    def rarity_color(self) -> int: 
        return conf.character_colors.get(self.rarity.value, 0x979C9F)

    @property
    def roll_chance(self) -> float: 
        return self.chance * conf.character_chances.get(self.rarity.value, 0)

    @property 
    def character_rating(self) -> float: 
        chance = self.roll_chance
        if chance <= 0:
            return 100.0
        log_rarity = -log10(chance)
        rating = (log_rarity - 0.6726) * 19.92 + 12.0
        return round(max(0.0, min(rating, 100.0)), 2)

    @property 
    def price(self) -> float: 
        return normalize_value(0.4 + (self.character_rating - 12.0) * (5.0 - 0.4) / (100.0 - 12.0))