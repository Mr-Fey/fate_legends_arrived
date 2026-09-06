from disnake import ButtonStyle, Color, MediaGalleryItem, ui, Locale

from db.models import Character, User
from utils.localization import translate
from utils.types import Result

from ._general import back_to_profile_button, character_info_select, quote


def character_control_template(
    user: User,
    locale: Locale = None,
) -> ui.UIComponent:
    return [
        ui.Container(
            back_to_profile_button(user.id),
            ui.Separator(),
            ui.TextDisplay(
                translate("profile_template_title", locale, user=f"<@{user.id}>")
            ),
            ui.Separator(),
            ui.MediaGallery(
                MediaGalleryItem(
                    media="attachment://characters_banner.png",
                )
            ),
            *([character_info_select(user)]) if user.len_characters else (),
            ui.ActionRow(
                ui.Button(
                    label="Призвать нового слугу",
                    style=ButtonStyle.primary,
                    custom_id=f"summon_character:{user.id}",
                ),
                ui.Button(
                    label="Рассееть слугу",
                    style=ButtonStyle.danger,
                    custom_id=f"sell_character_menu:{user.id}",
                    disabled=True,
                ),
                ui.Button(
                    label="Прокачать слугу",
                    style=ButtonStyle.secondary,
                    custom_id=f"upgrade_character_menu:{user.id}",
                    disabled=True,
                ),
            ),
        )
    ]


def character_info_template(character: Character) -> ui.UIComponent:
    return [
        ui.Container(
            ui.Section(
                ui.TextDisplay(f"# {character.name} {character.character_rating}♦CR"),
                accessory=ui.Thumbnail(character.icon or "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Question_Mark.svg/960px-Question_Mark.svg.png?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=thumbnail")
            ),
            ui.Separator(),
            ui.TextDisplay(character.full_description),
            ui.Separator(),
            ui.MediaGallery(
                *(
                    MediaGalleryItem(
                        media=img,
                    )
                    for img in character.banners
                )
            ),
            accent_colour=Color(int(character.rarity_color, 16)),
        )
    ]


def summon_character_menu_template(user: User) -> ui.UIComponent:
    return [
        ui.Container(
            back_to_profile_button(user.id),
            ui.MediaGallery(
                MediaGalleryItem(
                    media="https://static2.klipy.com/ii/4e7bea9f7a3371424e6c16ebc93252fe/82/1e/1qvSh3ZiyEmMZU7GX99r.gif"
                ),
            ),
            ui.TextDisplay(f"### - {quote()}"),
            ui.ActionRow(
                ui.Button(
                    label=f"Обычный ({user.quartz})",
                    custom_id=f"common_summon:{user.id}",
                    style=ButtonStyle.secondary,
                ),
                ui.Button(
                    label=f"Редкий ({user.negative_quartz})",
                    custom_id=f"negative_summon:{user.id}",
                    style=ButtonStyle.secondary,
                ),
                ui.Button(
                    label=f"Легендарный ({user.gold_quartz})",
                    custom_id=f"gold_summon:{user.id}",
                    style=ButtonStyle.secondary,
                ),
            ),
        )
    ]


def summon_character_template(user: User) -> ui.UIComponent:
    return [
        ui.Container(
            ui.MediaGallery(
                MediaGalleryItem(
                    media="https://64.media.tumblr.com/681134f362163899943e23f777ee25dd/4c2815bb07a2ccb7-87/s540x810/1001e0145cead8d4ceaa9f55fcf5792b0953f476.gif"
                ),
            ),
            ui.TextDisplay(f"### - {quote()}"),
            ui.ActionRow(
                ui.Button(
                    label=f"Обычный ({user.quartz})",
                    custom_id=f"common_summon:{user.id}",
                    style=ButtonStyle.secondary,
                    disabled=True,
                ),
                ui.Button(
                    label=f"Редкий ({user.negative_quartz})",
                    custom_id=f"negative_summon:{user.id}",
                    style=ButtonStyle.secondary,
                    disabled=True,
                ),
                ui.Button(
                    label=f"Легендарный ({user.gold_quartz})",
                    custom_id=f"gold_summon:{user.id}",
                    style=ButtonStyle.secondary,
                    disabled=True,
                ),
            ),
        )
    ]


def summon_character_result_template(
    author_id: int,
    result: Result,
    description: str = None, 
) -> ui.UIComponent:
    if result.type == "character":
        character = result.character
        description = character.description
        image = character.icon
    elif result.type == "money":
        image = "https://i0.wp.com/media4.giphy.com/media/b96PWARO1Z5YY/giphy.gif"
    elif result.type == "quartz":
        image = "https://tenor.com/bBtdG.gif"
    elif result.type == "nothing":
        image = "https://media.tenor.com/x8v1oNUOmg4AAAAM/rickroll-roll.gif"

    return [
        ui.Container(
            ui.Section(
                ui.TextDisplay(description or result.description), 
                accessory=ui.Thumbnail(image)
            ),

            *(
                [
                    ui.ActionRow(
                        ui.Button(
                            label="Принять слугу", 
                            style=ButtonStyle.green, 
                            custom_id=f"save_character:{author_id}:{character.id}", 
                        ), 
                        ui.Button(
                            label=f"Рассеить слугу ({character.price})", 
                            style=ButtonStyle.danger, 
                            custom_id=f"sell_character:{author_id}:{character.id}", 
                        )
                    ) 
                ] if result.type == "character" else []
            ), 

            ui.ActionRow(
                ui.Button(
                    label="Новая попытка", 
                    style=ButtonStyle.secondary, 
                    custom_id=f"summon_character:{author_id}"
                )
            )
        )
    ]


def summon_character_final_template(
    author_id: int,
    character: Character,
    is_saved: bool = True,
) -> ui.UIComponent:
    text = "сохранен" if is_saved else "рассеен"
    return [
        ui.Container(
            ui.Section(
                ui.TextDisplay(f"## {character.name} {text}"),
                accessory=ui.Thumbnail(character.icon)
            ),
            ui.ActionRow(
                ui.Button(
                    label="Новая попытка", 
                    style=ButtonStyle.secondary, 
                    custom_id=f"summon_character:{author_id}"
                )
            )
        )
    ]
