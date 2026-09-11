import disnake
from bot import Bot
from disnake.ext import commands

from collections import defaultdict
from utils.templates import edit_member_quartz_template 
from utils.localization import translate
from utils.injections import (
    Callback,
    custom_id_check, 
    callback_data_injection,
)


class editMemberListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.data = defaultdict(dict)

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_quartz_user")
    @callback_data_injection()
    async def edit_member_quartz_user(
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
        self.data[f"{inter.message.id}"]["user"] = inter.values[0] 

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_quartz_type")
    @callback_data_injection()
    async def edit_member_quartz_type(
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
        self.data[f"{inter.message.id}"]["quartz_type"] = inter.values[0] 

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_quartz_value")
    @callback_data_injection()
    async def edit_member_quartz_value(
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
        self.data[f"{inter.message.id}"]["value"] = inter.values[0] 

    @commands.Cog.listener(name="on_dropdown")
    @custom_id_check("edit_member_quartz_request")
    @callback_data_injection()
    async def edit_member_quartz_request(
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
        self.data[f"{inter.message.id}"]["request"] = inter.values[0] 

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("edit_member_quartz_confirm")
    @callback_data_injection()
    async def listener_name_listener(
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

        key = f"{inter.message.id}"
        user: disnake.Member = self.data[key].get("user")
        quartz_type = self.data[key].get("quartz_type")
        request = self.data[key].get("request")
        pre_value = int(self.data[key].get("value", 0))
        value = -pre_value if request == "remove" else +pre_value

        if any(not i for i in [user, quartz_type, request, value]): 
            return await inter.send(
                translate("edit_member_quartz_decline", inter.locale), 
                ephemeral=True, 
            )

        await self.bot.db.update_user_money(
            user_id=user.id, 
            type=quartz_type, 
            delta=value, 
        )
        await inter.send(
            translate("edit_member_quartz_complited", inter.locale), 
            ephemeral=True,
        )
        await inter.edit_original_message(
            coomponents=edit_member_quartz_template(inter.author.id), 
            flags=disnake.MessageFlags(is_components_v2=True)
        )
        del self.data[str(inter.message.id)]
        await user.send(
            translate(
                "edit_member_quartz_notify",
                inter.locale,
                quartz=f"{value}{self.bot.conf.quartz_emojis[quartz_type]}"
            )
        )


def setup(bot: Bot) -> None:
    bot.add_cog(editMemberListener(bot))
