import random
import asyncio
import disnake

from settings import conf
from settings import roll_schedule
from utils.localization import translate
from utils.templates import summon_character_result_template, summon_character_template
from utils.types import Callback, Result


async def summon_character(
    self,
    inter: disnake.MessageInteraction,
    callback: Callback,
    quartz_type: str,
):
    if not callback.author_id or inter.author.id != callback.author_id:
        return await inter.send(
            translate("not_from_author_interaction_error", inter.locale),
            ephemeral=True,
        )

    user = await self.bot.db.get_user(inter.author.id)
    if not user or getattr(user, quartz_type, 0) < 1:
        return await inter.send(
            translate("not_enough_quartz_error", inter.locale),
            ephemeral=True,
        )

    await inter.edit_original_message(
        components=summon_character_template(user),
        flags=disnake.MessageFlags(is_components_v2=True),
    )

    character = None
    roll_data = None
    for _, roll_config in roll_schedule.__dict__.items():
        if isinstance(roll_config, dict) and roll_config.get("price") == quartz_type:
            roll_data = roll_config
            break

    drop_data = roll_data["drop"]
    data = {"population": [], "weights": []}

    for k, v in drop_data.items(): 
        data['population'].append(k)
        data['weights'].append(v['chance'])

    choice = random.choices(
        **data,
        k=1,
    )[0]

    drop = drop_data[choice]
    
    if drop['type'] == "character":
        character = await self.bot.db.get_character_by_name(drop['character_name'])
    elif drop['type'] == 'quartz':
        await self.bot.db.update_user_money(user_id=user.id, type=conf.quartz_types.get(drop['quartz_type'], 'quartz'), delta=drop['amount'])
    elif drop['type'] == 'money':
        await self.bot.client.update_user_balance(inter.guild_id, user.id, bank=+drop['amount'])

    result = Result(
        type=drop['type'],
        description=drop['description'],
        character=character,
    )
    await self.bot.db.update_user_money(user_id=user.id, type=conf.quartz_types.get(quartz_type, 'quartz'), delta=-1)
    await asyncio.sleep(4)
    await inter.edit_original_message(
        components=summon_character_result_template(user.id, result),
        flags=disnake.MessageFlags(is_components_v2=True),
    )