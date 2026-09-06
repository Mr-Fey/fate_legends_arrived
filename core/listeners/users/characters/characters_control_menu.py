import disnake
from bot import Bot
from disnake.ext import commands

from utils.imgen import characters_image_generate
from utils.injections import (
    Callback,
    callback_data_injection,
    custom_id_check,
)
from utils.localization import translate
from utils.templates import character_control_template


class CharacterControlMenuListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("characters_control")
    @callback_data_injection()
    async def characters_control_menu_listener(
        self,
        inter: disnake.MessageInteraction,
        callback: Callback,
    ) -> None:
        await inter.response.defer(ephemeral=True)

        if not callback.author_id or inter.author.id != callback.author_id:
            return await inter.send(
                translate("not_from_author_interaction_error", inter.locale),
                ephemeral=True,
            )

        user = await self.bot.db.get_user(inter.author.id)
        banner = await characters_image_generate(user.characters, user.banner_id)

        await inter.edit_original_message(
            file=banner,
            components=character_control_template(user, locale=inter.locale),
            flags=disnake.MessageFlags(is_components_v2=True),
        )


def setup(bot: Bot) -> None:
    bot.add_cog(CharacterControlMenuListener(bot))