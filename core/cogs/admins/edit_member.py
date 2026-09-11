import disnake
from bot import Bot
from disnake.ext import commands
from disnake.i18n import Localised
from utils.templates import edit_member_quartz_template 


class EditMembedCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
 
    @commands.slash_command(name="edit")
    async def edit_command(self, inter): pass 

    @edit_command.sub_command(
        name="quartz", 
        description=Localised("Edit member's quartz", key="edit_quartz_command_description")
    )
    @commands.has_permissions(administrator=True)
    async def edit_quartz_command(
        self, 
        inter: disnake.AppCmdInter, 
    ): 
        await inter.response.defer()

        await inter.send(
            components=edit_member_quartz_template(inter.author.id), 
            flags=disnake.MessageFlags(is_components_v2=True)
        )


def setup(bot: Bot) -> None:
    bot.add_cog(EditMembedCog(bot))