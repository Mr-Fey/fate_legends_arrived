from disnake import (
    ui,
    Locale,
    ButtonStyle,
    MediaGalleryItem,
)

from db.models import User
from utils.imgen import _total_banners
from settings import conf
from utils.economy import get_money_draw
from utils.localization import translate

from ._general import (
    character_info_select, 
    back_to_profile_button, 
)



def profile_template(
    is_author: bool,
    user: User,
    yens: int, 
    locale: object = None,
) -> ui.UIComponent:
    return [
        ui.Container(
            ui.TextDisplay(
                translate("profile_template_title", locale, user=f"<@{user.id}>")
            ),
            ui.Separator(),
            *(
                ui.Section(
                    ui.TextDisplay(
                        get_money_draw(
                            value=getattr(user, conf.quartz_types.get(m_type, 'quartz')),
                            type=m_type,
                        ),
                    ),
                    accessory=ui.Button(
                        label="Перевести в 💴", 
                        custom_id=f"exchange_quartz:{idx}",
                        disabled=not is_author,
                    ), 
                ) for idx, (m_type) in enumerate(["quartz", "negative_quartz", "gold_quartz"])
            ),
            ui.Section(
                ui.TextDisplay(f"{yens:,}💴"),
                accessory=ui.Button(
                    label="Перевести в СК", 
                    custom_id=f"exchange_money:{user.id}", 
                    disabled=not is_author, 
                )
            ),
            ui.Separator(),
            ui.MediaGallery(
                MediaGalleryItem(
                    media="attachment://characters_banner.png",
                )
            ),
            *([character_info_select(user)]) if user.len_characters else (),
            ui.Separator(),
            *([ui.ActionRow(
                ui.Button(
                    label="Управление слугами",
                    style=ButtonStyle.primary,
                    custom_id=f"characters_control:{user.id}",
                ),
                ui.Button(
                    label="Редактор профиля",
                    style=ButtonStyle.danger,
                    custom_id=f"profile_control:{user.id}",
                ),
                ui.Button(
                    label="Инвентарь",
                    style=ButtonStyle.secondary,
                    custom_id=f"inventory:{user.id}",
                    disabled=True, 
                ),
            )]) if is_author else (),
        )
    ]


def profile_controle_template(user: User, locale: Locale) -> ui.UIComponent: 
    return [
        ui.Container(
            back_to_profile_button(user.id),
            ui.Separator(), 
            ui.Section(
                ui.TextDisplay(translate("banner", locale)), 
                accessory=ui.Button(
                    label="Изменить", 
                    style=ButtonStyle.secondary,
                    custom_id=f"edit_banner:{user.id}", 
                )
            ),
            ui.MediaGallery(
                MediaGalleryItem(f"attachment://background.png")
            ),
            ui.Separator(),
            ui.Section(
                ui.TextDisplay(translate("inkognito", locale)), 
                accessory=ui.Button(
                    label="Включено" if user.is_inkognito else "Выключено", 
                    style=ButtonStyle.success if user.is_inkognito else ButtonStyle.danger,
                    custom_id=f"edit_inkognito:{user.id}", 
                )
            )
        )
    ] 

def profile_banner_choice_template(author_id: int, message_id: int, banner_id: int) -> ui.UIComponent: 
    previous_id = (banner_id - 1) % _total_banners
    next_id = (banner_id + 1) % _total_banners

    return [
        ui.Container(
            ui.MediaGallery(
                MediaGalleryItem("attachment://background.png", description=str(message_id)), 
            ), 
            ui.ActionRow(
                ui.Button(
                    label="⬅", 
                    custom_id=f"banner_choice:{author_id}:{previous_id}", 
                ), 
                ui.Button(
                    label="Принять", 
                    custom_id=f"banner_choice_accept:{author_id}:{banner_id}", 
                ), 
                ui.Button(
                    label="⮕", 
                    custom_id=f"banner_choice:{author_id}:{next_id}", 
                )
            )
        )
    ]