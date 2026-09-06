import disnake
from bot import Bot
from disnake.ext import commands

from utils.localization import translate
from utils.imgen import characters_image_generate
from utils.templates import (
    profile_template,
)
from utils.injections import (
    Callback, 
    custom_id_check, 
    callback_data_injection,
)


class ExchangeListener(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def exchange(self, inter: disnake.MessageInteraction, types: tuple) -> int: 
        info = self.bot.conf.exchange_info[types[0]]
        if types[0] == "yens_to_quartz": 
            await self.bot.db.update_user_money(inter.author.id, info['quartz_type'], +info['quartz'])
            balance = await self.bot.client.update_user_balance(inter.guild_id, inter.author.id, bank=-info["yen"])
        else: 
            await self.bot.db.update_user_money(inter.author.id, types[1], -1)
            balance = await self.bot.client.update_user_balance(inter.guild_id, inter.author.id, bank=+info[types[1]])
        return balance.total

    @commands.Cog.listener(name="on_button_click")
    @custom_id_check("exchange_money")
    @callback_data_injection()
    async def exchange_money_listener(
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

        info = self.bot.conf.exchange_info["yens_to_quartz"]
        balance = await self.bot.client.get_user_balance(inter.guild_id, inter.author.id)

        if balance.total < info["yen"]: 
            return await inter.send(
                translate("no_money_error", inter.locale), 
                ephemeral=True, 
            )
        
        await self.bot.db.update_user_money(inter.author.id, info['quartz_type'], +info['quartz'])

        user = await self.bot.db.get_user(inter.author.id)
        balance = await self.bot.client.update_user_balance(inter.guild_id, inter.author.id, bank=-info["yen"])
        banner = await characters_image_generate(user.characters, user.banner_id)

        await inter.edit_original_message(
            file=banner,  
            components=profile_template(True, user, balance.total, inter.locale),
            flags=disnake.MessageFlags(is_components_v2=True, ephemeral=user.is_inkognito),
        )
        

def setup(bot: Bot) -> None:
    bot.add_cog(ExchangeListener(bot))