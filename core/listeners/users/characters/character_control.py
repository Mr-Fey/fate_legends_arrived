import random
import disnake
from bot import Bot
from disnake.ext import commands
from datetime import datetime, timedelta, timezone

from utils.localization import translate
from utils.templates import summon_character_final_template
from utils.injections import (
    Callback, 
    custom_id_check, 
    callback_data_injection,
)


class CharacterControlListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def is_expired(
        self, 
        inter: disnake.MessageInteraction, 
    ) -> bool: 
        message = inter.message
        timeout = datetime.now(timezone.utc) - message.edited_at or message.created_at
        return timeout > timedelta(minutes=5)

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("save_character")
    @callback_data_injection()
    async def save_character(
        self,
        inter: disnake.MessageInteraction,
        callback: Callback, 
    ) -> None:
        await inter.response.defer(ephemeral=True)

        if self.is_expired(inter):
            return await inter.send(
                translate("expired_error", inter.locale),
                ephemeral=True,
            )
        
        if not callback.author_id or inter.author.id != callback.author_id:
            return await inter.send(
                translate("not_from_author_interaction_error", inter.locale),
                ephemeral=True,
            )
        if not callback.character_id: 
            return await inter.send(
                translate("unknown_error", inter.locale), 
                ephemeral=True, 
            )

        user = await self.bot.db.get_user(callback.author_id)
        if user.len_free_characters_slots < 1: 
            return await inter.send(
                translate("no_free_characters_slots_error", inter.locale), 
                ephemeral=True, 
            )

        character = await self.bot.db.get_character_by_id(callback.character_id)
        image_url = random.choice(character.banners) if len(character.banners) > 0 else character.banners[0]
        await self.bot.db.update_user_character_slot(
            user_id=user.id, 
            slot_index=user.free_characters_slots[0].index,
            character_id=callback.character_id, 
            image_url=image_url, 
        )
        await inter.edit_original_message(
            components=summon_character_final_template(inter.author.id, character, True), 
            flags=disnake.MessageFlags(is_components_v2=True), 
        )

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("sell_character")
    @callback_data_injection()
    async def sell_character(
        self,
        inter: disnake.MessageInteraction,
        callback: Callback, 
    ) -> None:
        await inter.response.defer(ephemeral=True)

        if self.is_expired(inter):
            return await inter.send(
                translate("expired_error", inter.locale),
                ephemeral=True,
            )

        if not callback.author_id or inter.author.id != callback.author_id:
            return await inter.send(
                translate("not_from_author_interaction_error", inter.locale),
                ephemeral=True,
            )
        if not callback.character_id: 
            return await inter.send(
                translate("unknown_error", inter.locale), 
                ephemeral=True, 
            )

        user = await self.bot.db.get_user(callback.author_id)
        if user.len_free_characters_slots < 1: 
            return await inter.send(
                translate("no_free_characters_slots_for_sell_error", inter.locale), 
                ephemeral=True, 
            )

        character = await self.bot.db.get_character_by_id(callback.character_id)
        await self.bot.db.update_user_money(
            user_id=user.id, 
            type="quartz", #TODO временно 
            delta=+character.price
        )
        await inter.edit_original_message(
            components=summon_character_final_template(inter.author.id, character, False), 
            flags=disnake.MessageFlags(is_components_v2=True), 
        )


def setup(bot: Bot) -> None:
    bot.add_cog(CharacterControlListener(bot))
