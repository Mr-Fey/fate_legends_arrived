import sqlalchemy as sa 
from .base import BaseModel
from typing import Optional

from utils.enums import ItemRarity
from sqlalchemy.orm import Mapped, mapped_column


class Item(BaseModel): 
    id: Mapped[int] = mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    price: Mapped[float] = mapped_column(sa.Float(), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(sa.Text(), nullable=True)

    description: Mapped[str] = mapped_column(sa.Text(), nullable=False)
    full_description: Mapped[str] = mapped_column(sa.Text(), nullable=False)

    rarity: Mapped[ItemRarity] = mapped_column(sa.Enum(ItemRarity), nullable=False)
    chance: Mapped[float] = mapped_column(sa.Float(), nullable=False) # with this chance in item's rarity will be "spawn" in create shop task

    stack_limit: Mapped[int] = mapped_column(
        "limit",
        sa.Integer(),
        default=1,
        server_default="1",
        nullable=False,
    )
    purchase_text: Mapped[str] = mapped_column(sa.Text(), nullable=False, default="Все, давай шуруй уже!")
    purchase_quantity: Mapped[int] = mapped_column(
        sa.Integer(),
        default=1,
        server_default="1",
        nullable=False,
    ) 

    @property
    def is_stackable(self) -> bool:
        return self.stack_limit > 1
