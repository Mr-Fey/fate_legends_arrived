import disnake
from bot import Bot
from disnake import ui

from utils.localization import translate


def info_template(
    bot: Bot,
    latency: float,
    guild_name: str,
    member_count: int,
    bot_count: int,
    locale: object = None,
) -> ui.UIComponent:
    return [
        ui.Container(
            ui.TextDisplay(
                translate("bot_info_title", locale, user=bot.user.name)
            ),
            ui.Separator(),
            ui.TextDisplay(
                translate("bot_info_latency", locale, latency=round(latency, 2))
            ),
            ui.TextDisplay(translate("bot_info_creator", locale)),
            ui.Separator(),
            ui.TextDisplay(
                translate("bot_info_guild_name", locale, guild_name=guild_name)
            ),
            ui.TextDisplay(
                translate("bot_info_member_count", locale, member_count=member_count)
            ),
            ui.TextDisplay(
                translate("bot_info_bot_count", locale, bot_count=bot_count)
            ),
            accent_colour=disnake.Color(0xFFFF00),
        )
    ]