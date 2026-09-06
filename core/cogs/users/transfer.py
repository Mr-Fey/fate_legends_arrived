import disnake
from bot import Bot
from db.models import User 

from disnake.ext import commands
from disnake.i18n import Localised

from utils.localization import translate
from utils.autocomplieters import member_characters


class TransferCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.slash_command(
        name="transfer", 
        description="Transfer Command", 
    )
    async def transfer(self, inter): pass 

    @transfer.sub_command(
        name="servant", 
        description=Localised("Transfer Servant to another Person", key="transfer_servant_description")
    ) 
    async def transfer_servant(
        self, 
        inter: disnake.AppCmdInter, 
        user: User, 
        servant: str = commands.Param(
            name="servant", 
            description=Localised("Servant to transfer", key="transfer_servant_arg_description"),
        ), 
        mbr: disnake.Member = commands.Param(
            name="member", 
            description=Localised("Member for transfer", key="transfer_servant_member_description")
        ), 
        comment: str = commands.Param(
            default=None,
            name="comment", 
            description=Localised("Optional comment, that you want show with transfer notify", key="transfer_servant_comment_description")
        )
    ): 
        await inter.response.defer(ephemeral=True)

        if mbr.id == inter.author.id: 
            return await inter.send(
                Localised("You can't send it to yourself!", key="same_id_per_send_error"),
                ephemeral=True, 
            )

        member = await self.bot.db.create_or_get_user(id=mbr.id, quartz=1)
        characters = [c for c in user.characters_slots if c.name.lower() == servant.lower()]
        if not characters: 
            return await inter.send(translate("unknown_error", inter.locale))
        
        character = characters[0]

        if member.len_free_characters_slots <= 0: 
            return await inter.send(translate("transfer_servant_no_members_slots_error", inter.locale))

        free_slot = member.free_characters_slots[0]
        await self.bot.db.update_user_character_slot(
            user_id=member.id, 
            slot_index=free_slot.index, 
            character_id=character.character_id, 
            image_url=character.image_url,
        )
        await self.bot.db.update_user_character_slot(
            user_id=user.id, 
            slot_index=character.index, 
            character_id=None, 
            image_url=None,
        )

        await inter.send(
            translate(
                "transfer_servant_successfully",
                inter.locale,
                servant=character.name,
                member=mbr.mention,
            ),
        )
        await mbr.send(
            translate(
                "transfer_servant_successfully_notify",
                inter.locale,
                servant=character.name,
                slot_index=free_slot.index + 1,
                member=inter.author.mention,
                comment=comment or "-",
            ),
        )
        await self.bot.log(
            "💛", 
            f"{inter.author.mention} transferred {character.name} to {mbr.mention}"
        )

    @transfer_servant.autocomplete("servant")
    async def transfer_servant_autocomplete(
        self, 
        inter: disnake.AppCmdInter, 
        input: str, 
    ): 
        user = await self.bot.db.get_user(inter.author.id)
        return member_characters(inter, input, user)

def setup(bot: Bot) -> None:
    bot.add_cog(TransferCog(bot))
