import disnake
from bot import Bot
from disnake.ext import commands
from disnake.i18n import Localised


class TopCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="top", 
        description=Localised("Top Servant Ranking by CR value", key="top_command_description")
    )
    async def top(
        self, 
        inter: disnake.AppCmdInter,
    ): 
        await inter.response.defer()

        users = await self.bot.db.get_all_users()
        top = sorted(
            (
                (user.id, sum(character.character_rating for character in user.characters_slots or []))
                for user in users if user.characters_slots
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        await inter.send(
            embed=disnake.Embed(
                description="".join(
                    f"{idx}. <@{user_id}> - {rating:.2f}♦CR\n"
                    for idx, (user_id, rating) in enumerate(top[:10], 1)
                ), 
            ),
        )


def setup(bot: Bot) -> None:
    bot.add_cog(TopCog(bot))