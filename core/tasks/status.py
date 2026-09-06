import random
import disnake
import logging

from bot import Bot

from disnake.ext import tasks, commands


_log = logging.getLogger(__name__)


class StatusTask(commands.Cog): 
    def __init__(self, bot: Bot): 
        self.bot = bot  
        self.statuslist = bot.conf.statuslist


    @commands.Cog.listener()
    async def on_ready(self):
        if not self.status_task.is_running():
            self.status_task.start()

    @tasks.loop(minutes=15)
    async def status_task(self): 
        activity = random.choice(self.statuslist)
        
        await self.bot.change_presence(
            activity=disnake.CustomActivity(name=activity), 
            status=disnake.Status.idle,
        )

        _log.info("Статус обновлен: " + activity)


def setup(bot: Bot): 
    bot.add_cog(StatusTask(bot))