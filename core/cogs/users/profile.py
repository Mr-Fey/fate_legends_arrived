import disnake
from bot import Bot
from db.models import User

from disnake.ext import commands
from disnake.i18n import Localised

from utils.imgen import characters_image_generate
from utils.localization import translate
from utils.templates import profile_template


class ProfileCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="profile",
        description=Localised("View your profile", key="profile_command_description"),
    )
    async def profile(
        self,
        inter: disnake.AppCmdInter,
        user: User, #Чисто для injection
        member: disnake.Member = commands.Param(
            default=lambda inter: inter.author,
            description=Localised("View member's profile", key="profile_member_description"),
        ),
    ):
        await inter.response.defer(ephemeral=user.is_inkognito)
        
        user = await self.bot.db.get_user(member.id)
        is_author = inter.author.id == member.id
        if user.is_inkognito and not is_author:
            return await inter.send(
                translate("profile_inkognito_error", inter.locale),
                ephemeral=True,
            )

        banner = await characters_image_generate(user.characters, user.banner_id)
        yens = await self.bot.client.get_user_balance(inter.guild_id, user.id)

        await inter.send(
            file=banner, 
            components=profile_template(is_author, user, yens.total, inter.locale),
            flags=disnake.MessageFlags(is_components_v2=True, ephemeral=user.is_inkognito),
        )


def setup(bot: Bot) -> None:
    bot.add_cog(ProfileCog(bot))