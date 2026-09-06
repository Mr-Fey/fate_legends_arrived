import disnake
from bot import Bot
from db.models import User
from disnake.i18n import Localised
from disnake.ext import commands

from utils.economy import get_money_draw
from utils.localization import translate
from utils.autocomplieters import member_characters


class DisperseCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="disperse", 
        description=Localised("Disperse the Servant", key="disperse_command_description")
    )
    async def disperse(
        self, 
        inter: disnake.AppCmdInter, 
        user: User, 
        servant: str = commands.Param(
            name="servant", 
            description=Localised("Servant to disperse", key="disperse_servant_description"),
        )
    ): 
        await inter.response.defer(ephemeral=user.is_inkognito)

        character = [c for c in user.characters_slots if c.name.lower() == servant.strip().lower()][0]
        await self.bot.db.update_user_character_slot(
            user_id=user.id, 
            slot_index=character.index, 
            character_id=None, 
        )
        await self.bot.db.update_user_money(
            user_id=user.id, 
            type="quartz", #TODO пока что
            delta=+character.price, 
        )
        await inter.send(
            translate("disperse_successfully", inter.locale).format(
                servant=character.name,
                price=get_money_draw(character.price, "quartz"),
            )
        )

    @disperse.autocomplete("servant")
    async def disperse_servant_autocomplete(
        self, 
        inter: disnake.AppCmdInter, 
        input: str, 
    ): 
        user = await self.bot.db.get_user(inter.author.id)
        return member_characters(inter, input, user)
        


def setup(bot: Bot) -> None:
    bot.add_cog(DisperseCog(bot))
