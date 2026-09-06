import disnake 
import logging
from typing import List
from db.models import User, Character


_log = logging.getLogger(__name__)


def member_characters(
    inter: disnake.AppCmdInter, 
    input: str, 
    user: User, 
) -> list: 
    try:
        return [
            c.name
            for c in user.characters_slots
            if c.name
            and input.casefold() in c.name.casefold()
        ]
    except Exception as e:
        _log.error(f"Member Characters Autocomplete error: {e}")
        return []


def characters(
    inter: disnake.AppCmdInter, 
    input: str, 
    characters: List[Character], 
) -> list: 
    try: 
        return [
            c.name 
            for c in characters
            if input.casefold() in c.name.casefold()
        ]
    except Exception as e:
        _log.error(f"Characters Autocomplete error: {e}")
        return []