import random
import disnake
from bot import Bot
from disnake.ext import commands

from collections import defaultdict
from utils.templates import edit_member_character_template 
from utils.localization import translate
from utils.injections import (
    Callback,
    custom_id_check, 
    callback_data_injection,
)


class editMemberCharacterListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.data = defaultdict(dict)

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_character_user")
    @callback_data_injection()
    async def edit_member_character_user(
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
        self.data[str(inter.message.id)]["user_id"] = inter.values[0] 

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_character_id")
    @callback_data_injection()
    async def edit_member_character_id(
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

        self.data[str(inter.message.id)]['character_id'] = int(inter.values[0])

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_character_slot_index")
    @callback_data_injection()
    async def edit_member_character_slot_index(
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
        self.data[str(inter.message.id)]['slot_index'] = int(inter.values[0])


    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("edit_member_character_confirm")
    async def edit_member_character_confirm(
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

        data = self.data[str(inter.message.id)]
        user_id = data.get('user_id')
        character_id = data.get('character_id')
        slot_index = data.get('slot_index')
        character_name = translate("edit_member_character_name", inter.locale)
        image_url = None

        pre_characters = await self.bot.db.get_all_characters()
        characters = {c.name: c.id for c in pre_characters}

        if any(i is None for i in [user_id, character_id, slot_index]): 
            return await inter.send(
                translate("edit_member_not_full_info", inter.locale), 
                ephemeral=True, 
            )

        if character_id != 0: 
            character = await self.bot.db.get_character_by_id(character_id)
            character_name = character.name
            image_url = random.choice(character.banners) if len(character.banners) > 0 else character.banners[0]

        await self.bot.db.update_user_character_slot(
            user_id=user_id, 
            slot_index=slot_index, 
            character_id=character_id, 
            image_url=image_url, 
        )

        await inter.send(
            translate("edit_member_character_complited", inter.locale), 
            ephemeral=True,
        )
        await inter.message.edit(
            components=edit_member_character_template(inter.author.id, characters), 
            flags=disnake.MessageFlags(is_components_v2=True)
        )

        del self.data[str(inter.message.id)]

        user = await self.bot.fetch_user(user_id)
        await user.send(
            translate(
                "edit_member_character_notify",
                inter.locale,
                servant=character_name, 
                slot_index=slot_index + 1,
            )
        )


def setup(bot: Bot) -> None: 
    bot.add_cog(editMemberCharacterListener(bot))