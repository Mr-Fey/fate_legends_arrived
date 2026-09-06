import disnake
from bot import Bot
from db.models import User
from disnake.ext import commands
from disnake.i18n import Localised

from utils.localization import translate
from utils.templates import summon_character_menu_template


class SummonCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="summon",
        description=Localised("Summon Servant", key="summon_command_description"),
    )
    async def summon(
        self,
        inter: disnake.AppCmdInter,
        user: User, 
    ):
        await inter.response.defer(ephemeral=user.is_inkognito)

        await inter.send(
            components=summon_character_menu_template(user),
            flags=disnake.MessageFlags(is_components_v2=True),
            ephemeral=user.is_inkognito,
        )


def setup(bot: Bot) -> None:
    bot.add_cog(SummonCog(bot))