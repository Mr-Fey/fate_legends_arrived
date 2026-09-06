import disnake

from bot import Bot
from typing import List 
from db.models import Character

from disnake.ext import commands
from disnake.i18n import Localised

from utils.localization import translate
from utils.autocomplieters import characters as ca
from utils.templates import character_info_template


class LibraryCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.characters: List[Character] = None

    @commands.slash_command(
        name="library", 
        description=Localised("Library with information about Servants", key="library_description")
    ) 
    async def library(
        self, 
        inter: disnake.AppCmdInter, 
        servant: str = commands.Param(
            name="servant", 
            description=Localised("Servant you want to know information about", key="library_servant_description"),
        )
    ): 
        await inter.response.defer(ephemeral=True)

        character = await self.bot.db.get_character_by_name(servant)
        if not character: 
            await self.bot.log(
                "‼‼",
                "Character Info (library) Error: Problem with Name",
                sep="\n",
            )
            return await inter.send(
                translate("unknown_error", inter.locale),
                ephemeral=True,
            )

        await inter.send(
            components=character_info_template(character), 
            flags=disnake.MessageFlags(is_components_v2=True, ephemeral=True), 
        )

    @commands.Cog.listener("on_ready")
    async def on_library_cog_ready(self): 
        self.characters = await self.bot.db.get_all_characters()

    @library.autocomplete("servant")
    async def servant_servant_autocomplete(
        self, 
        inter: disnake.AppCmdInter, 
        input: str, 
    ): 
        return ca(inter, input, self.characters)
            

def setup(bot: Bot) -> None:
    bot.add_cog(LibraryCog(bot))