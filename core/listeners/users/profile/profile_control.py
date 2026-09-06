import disnake
from bot import Bot
from disnake.ext import commands

from utils.imgen import _backgrounds_path
from utils.localization import translate
from utils.injections import (
    Callback,
    custom_id_check, 
    callback_data_injection, 
)
from utils.templates import profile_controle_template


class EditProfileMenu(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("profile_control")
    @callback_data_injection()
    async def profile_control_listener(
        self,
        inter: disnake.MessageInteraction,
        callback: Callback, 
    ) -> None:
        await inter.response.defer()
        
        if not callback.author_id or inter.author.id != callback.author_id:
            return await inter.send(
                translate("not_from_author_interaction_error", inter.locale),
                ephemeral=True,
            )

        user = await self.bot.db.get_user(callback.author_id)
        banner = disnake.File(_backgrounds_path / f"background_{user.banner_id}.png", "background.png")

        await inter.edit_original_message(
            file=banner, 
            components=profile_controle_template(user, inter.locale), 
            flags=disnake.MessageFlags(is_components_v2=True)
        )
        

def setup(bot: Bot) -> None:
    bot.add_cog(EditProfileMenu(bot))