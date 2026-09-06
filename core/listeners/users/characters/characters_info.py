import disnake
from bot import Bot
from disnake.ext import commands

from utils.injections import (
    Callback,
    callback_data_injection,
    custom_id_check,
)
from utils.localization import translate
from utils.templates import character_info_template


class CharacterInfoListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("character_info")
    @callback_data_injection()
    async def character_info_listener(
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

        value = inter.values[0].split(":")
        character_id = value[0]
        if not character_id.isdigit():
            await self.bot.log(
                "‼‼",
                "Character Info Error: Problem with ID",
                sep="\n",
            )
            return await inter.send(
                translate("unknown_error", inter.locale),
                ephemeral=True,
            )

        character = await self.bot.db.get_character_by_id(character_id)
        await inter.send(
            components=character_info_template(character),
            flags=disnake.MessageFlags(is_components_v2=True),
            ephemeral=True,
        )


def setup(bot: Bot) -> None:
    bot.add_cog(CharacterInfoListener(bot))
