import disnake
from bot import Bot
from disnake.ext import commands

from utils.templates import inventory_menu_template
from utils.localization import translate
from utils.injections import (
    Callback, 
    custom_id_check,
    callback_data_injection,  
)


class InventoryMenuListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("inventory")
    @callback_data_injection()
    async def inventory_menu_listener(
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
            return await inter.send(
                translate("no_items_in_inventory", inter.locale), 
                ephemeral=True, 
            )

        await inter.edit_original_message(
            components=inventory_menu_template(user, 0, inter.locale), 
            flags=disnake.MessageFlags(is_components_v2=True), 
        )
        
        

def setup(bot: Bot) -> None:
    bot.add_cog(InventoryMenuListener(bot))