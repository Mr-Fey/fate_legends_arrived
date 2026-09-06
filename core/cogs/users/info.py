import disnake
from bot import Bot

from disnake.ext import commands
from disnake.i18n import Localised

from utils.localization import translate
from utils.templates import info_template


class InfoCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="info",
        description=Localised("Server and bot information", key="info_command_description"),
    )
    async def info(
        self,
        inter: disnake.AppCommandInter,
    ):
        await inter.response.defer()

        latency = self.bot.latency * 1000
        member_count = inter.guild.member_count
        bot_count = len(inter.guild.members) - member_count

        await inter.send(
            components=info_template(
                bot=self.bot,
                latency=latency,
                guild_name=inter.guild.name,
                member_count=member_count,
                bot_count=bot_count,
                locale=inter.locale,
            ),
            flags=disnake.MessageFlags(is_components_v2=True),
        )


def setup(bot: Bot) -> None:
    bot.add_cog(InfoCog(bot))