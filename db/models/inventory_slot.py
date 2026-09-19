import sqlalchemy as sa 
from .base import BaseModel
from typing import Optional, TYPE_CHECKING

from settings import conf

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

if TYPE_CHECKING: 
    from .user import User 
    from .item import Item


class InventorySlot(BaseModel): 
    id: Mapped[int] = mapped_column(
        sa.Integer(),
        primary_key=True,
        autoincrement=True,
    )

    index: Mapped[int] = mapped_column(sa.Integer(), nullable=False)  # номер слота
    quantity: Mapped[int] = mapped_column(sa.Integer(), default=0, nullable=False)

    is_rent: Mapped[bool] = mapped_column(sa.Boolean(), default=False, nullable=False)
    rent: Mapped[float] = mapped_column(sa.Float(), default=0, nullable=False)

    item_id: Mapped[Optional[int]] = mapped_column(
        sa.ForeignKey("items.id", ondelete="CASCADE"),
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="inventory",
        lazy="selectin",
    )
    item: Mapped["Item"] = relationship(
        "Item",
        lazy="selectin",
    )

    @property 
    def name(self) -> str: 
        return self.item.name 

    @property 
    def image_url(self) -> Optional[str]: 
        return self.item.image_url

    @property
    def price(self) -> float: 
        return f"{self.item.price}{conf.quartz_emojis['quartz']}"

    @property
    def description(self) -> float: 
        return self.item.description

    @property
    def full_description(self) -> float: 
        return self.item.full_description