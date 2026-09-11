import random 
from settings import cwd, conf
from utils.economy import get_money_draw
from db.models import User
from disnake import ui, SelectOption, ButtonStyle



QUOTE_PATH = cwd / "json" / "quotes.txt"
QUARTZ_TYPES_ENUMERATE = enumerate(["quartz", "negative_quartz", "gold_quartz"])


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


def exchange_buttons(user: User, is_author: bool) -> list[ui.Section]: 
    sections = []
    for idx, (m_type) in QUARTZ_TYPES_ENUMERATE: 
        sections.append(
            ui.Section(
                ui.TextDisplay(
                    get_money_draw(
                        value=getattr(user, conf.quartz_types.get(m_type, 'quartz')),
                        type=m_type,
                    ),
                ),
                accessory=ui.Button(
                    label="Перевести в 💴", 
                    custom_id=f"exchange_quartz:{user.id}:{idx}",
                    disabled=not is_author,
                ), 
            ) 
        )
    return sections


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