import disnake
from bot import Bot
from disnake.ext import commands

from utils.localization import translate
from utils.injections import (
    Callback,
    custom_id_check, 
    callback_data_injection, 
)
from utils.imgen import _backgrounds_path
from utils.templates import (
    profile_controle_template,
    profile_banner_choice_template,
    
)

class EditProfile(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("edit_inkognito")
    @callback_data_injection()
    async def edit_inkognito_listener(
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

        is_inkognito = inter.component.style == disnake.ButtonStyle.success
        user = await self.bot.db.update_user_profile_data(callback.author_id, inkognito=not is_inkognito)

        await inter.edit_original_message(
            files=inter.message.attachments, 
            components=profile_controle_template(user, inter.locale), 
            flags=disnake.MessageFlags(is_components_v2=True)
        )

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("edit_banner")
    @callback_data_injection()
    async def edit_banner(
        self, 
        inter: disnake.MessageInteraction, 
        callback: Callback, 
    ): 
        await inter.response.defer(ephemeral=True)

        if not callback.author_id or inter.author.id != callback.author_id:
            return await inter.send(
                translate("not_from_author_interaction_error", inter.locale),
                ephemeral=True,
            )

        banner = disnake.File(_backgrounds_path / "background_1.png", "background.png")

        await inter.send(
            file=banner,
            components=profile_banner_choice_template(callback.author_id, inter.message.id, 1),
            flags=disnake.MessageFlags(is_components_v2=True, ephemeral=True)
        )

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("banner_choice")
    @callback_data_injection()
    async def banner_choice(
        self, 
        inter: disnake.MessageInteraction, 
        callback: Callback, 
    ): 
        await inter.response.defer(ephemeral=True)

        container = inter.message.components[0]
        gallery = [c for c in container.children if isinstance(c, disnake.MediaGallery)][0]
        message_id = int(gallery.items[0].description)
        banner = disnake.File(_backgrounds_path / f"background_{callback.character_id}.png", "background.png")

        await inter.edit_original_response(
            file=banner, 
            components=profile_banner_choice_template(
                callback.author_id,
                message_id,
                callback.character_id,
            ),
            flags=disnake.MessageFlags(is_components_v2=True, ephemeral=True),
        )

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("banner_choice_accept")
    @callback_data_injection()
    async def banner_choice_accept(
        self, 
        inter: disnake.MessageInteraction, 
        callback: Callback, 
    ): 
        container = inter.message.components[0]
        gallery = [c for c in container.children if isinstance(c, disnake.MediaGallery)][0]
        message_id = int(gallery.items[0].description)

        banner = disnake.File(_backgrounds_path / f"background_{callback.character_id}.png", "background.png")

        user = await self.bot.db.update_user_profile_data(
            user_id=callback.author_id,
            banner_id=callback.character_id, 
        )

        try: 
            await inter.delete_original_message()
            msg = await inter.channel.fetch_message(message_id)
            if not msg: 
                return

            await msg.edit(
                file=banner, 
                components=profile_controle_template(user, inter.locale), 
                flags=disnake.MessageFlags(is_components_v2=True)
            )
        except: 
            pass


def setup(bot: Bot) -> None:
    bot.add_cog(EditProfile(bot))
