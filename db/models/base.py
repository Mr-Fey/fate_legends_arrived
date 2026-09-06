from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase, AsyncAttrs): 
    __abstract__ = True 

    @declared_attr.directive 
    def __tablename__(cls) -> str: 
        return f"{cls.__name__.lower()}s"