from dataclasses import dataclass
from db.models import Character


@dataclass
class Callback: 
    custom_id: str 
    author_id: int | None
    character_id: int | None


@dataclass
class Result: 
    type: str 
    description: str
    character: Character | None = None 