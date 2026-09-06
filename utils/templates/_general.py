import random 
from settings import cwd
from db.models import User
from disnake import ui, SelectOption, ButtonStyle



QUOTE_PATH = cwd / "json" / "quotes.txt"


def character_info_select(user: User) -> ui.ActionRow:
    return ui.ActionRow(
        ui.StringSelect(
            custom_id=f"character_info:{user.id}",
            placeholder="Подробнее...",
            options=[
                SelectOption(
                    label=char.name,
                    value=f"{char.character_id}:{char.index}",
                    description=f"Информация о {char.name}",
                )
                for char in user.characters_slots
            ],
        )
    )


def back_to_profile_button(user_id: int) -> ui.ActionRow: 
    return ui.ActionRow(
        ui.Button(
            label="❮", 
            style=ButtonStyle.secondary, 
            custom_id=f"back_to_profile:{user_id}", 
        )
    )


def quote() -> str: #TODO пока закинул сюда, потом найду местечко получше + кеш накину
    with QUOTE_PATH.open("r", encoding='utf-8')as f: 
        data = f.read()
    quotes = data.split("\n")
    return random.choice(quotes)