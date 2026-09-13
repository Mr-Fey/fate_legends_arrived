from disnake import (
    ui,
    Locale,
    ButtonStyle,
    SeparatorSpacing,
)

from db.models import User
from ._general import back_to_profile_button
from utils.localization import translate
from utils.types import Result


def inventory_menu_template(user: User, page_id: int, locale: Locale) -> ui.UIComponent: 
    start = page_id * 5 
    end = start + 5
    pages = user.len_inventory_items // 5
    items = user.inventory_items[start:end]

    return [
        ui.Container(
            back_to_profile_button(user.id),
            ui.Separator(),
            ui.TextDisplay(translate("user_inventory_page", locale, page=f"{page_id + 1}/{pages}")), 
            ui.Separator(), 
            *([    
                ui.Section(
                    ui.TextDisplay(f"{idx}. {i.name} - {i.quantity}"), 
                    ui.TextDisplay(translate("user_inventory_page_price", locale, price=i.price)),
                    ui.TextDisplay(translate("user_inventory_page_rent", locale, rent=i.rent if i.is_rent else "-")), 
                    ui.TextDisplay(f"{i.full_description}"), 
                    accessory=ui.Thumbnail(i.image_url or "https://cdn-icons-png.flaticon.com/512/46/46940.png")
                ), 
                ui.ActionRow(
                    ui.Button(
                        label="Использовать", 
                        style=ButtonStyle.secondary, 
                        custom_id=f"use_item:{user.id}:{i.id}", 
                    ), 
                    ui.Button(
                        label="Выкинуть", 
                        style=ButtonStyle.danger, 
                        custom_id=f"drop_item:{user.id}:{i.id}"
                    )
                )
            ] for idx, (i) in enumerate(items, start + 1)), 
            ui.Separator(spacing=SeparatorSpacing.large), 
            ui.ActionRow(
                ui.Button(
                    label="⬅", 
                    custom_id=f"inventory_pages_roll:{user.id}:{page_id - 1}",
                    disabled=page_id <= 0,  
                ), 
                ui.Button(
                    label="⮕", 
                    custom_id=f"inventory_pages_roll:{user.id}:{page_id + 1}", 
                    disabled=page_id >= pages, 
                )
            ), 
        )
    ]