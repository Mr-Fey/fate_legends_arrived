import disnake
from bot import Bot
from disnake.ext import commands

from utils.templates import (
    profile_template,
    inventory_menu_template,
)
from utils.localization import translate
from utils.injections import (
    Callback,
    custom_id_check, 
    callback_data_injection,
)


class InventoryPagesRollListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("custom_id")
    @callback_data_injection()
    async def inventory_pages_roll_listener(
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
        if not user.inventory_items: 
            balance = await self.bot.client.get_user_balance(inter.guild_id, inter.author.id)
            await inter.send(
                translate("no_items_in_inventory", inter.locale), 
                ephemeral=True, 
            )
            return await inter.edit_original_message(
                components=profile_template(True, user, balance.total, inter.locale), 
                flags=disnake.MessageFlags(is_components_v2=True), 
            )

        await inter.edit_original_message(
            components=inventory_menu_template(user, callback.character_id, inter.locale), 
            flags=disnake.MessageFlags(is_components_v2=True), 
        )

def setup(bot: Bot) -> None:
    bot.add_cog(InventoryPagesRollListener(bot))
