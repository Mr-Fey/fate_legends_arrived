import disnake
from bot import Bot
from disnake.ext import commands

from utils.general import summon_character
from utils.injections import (
    Callback,
    callback_data_injection,
    custom_id_check,
)
from utils.localization import translate
from utils.templates import summon_character_menu_template


class SummonCharacterListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("summon_character")
    @callback_data_injection()
    async def summon_character_listener(
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
        await inter.send(
            components=summon_character_menu_template(user),
            flags=disnake.MessageFlags(is_components_v2=True),
            ephemeral=user.is_inkognito,
        )

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("common_summon")
    @callback_data_injection()
    async def common_summon_listener(
        self,
        inter: disnake.MessageInteraction,
        callback: Callback,
    ):
        await inter.response.defer(ephemeral=True)
        await summon_character(self, inter, callback, "quartz")

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("negative_summon")
    @callback_data_injection()
    async def negative_summon_listener(
        self, 
        inter: disnake.MessageInteraction,
        callback: Callback,
    ):
        await inter.response.defer(ephemeral=True)
        await summon_character(self, inter, callback, "negative_quartz")

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("gold_summon")
    @callback_data_injection()
    async def gold_summon_listener(
        self, 
        inter: disnake.MessageInteraction,
        callback: Callback,
    ):
        await inter.response.defer(ephemeral=True)
        await summon_character(self, inter, callback, "gold_quartz")


def setup(bot: Bot) -> None:
    bot.add_cog(SummonCharacterListener(bot))