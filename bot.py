import logging 
import disnake 

from unbelievaboat import Client 

from disnake import Intents
from disnake.ext import commands 

from db.models import User
from db.database import Database
from settings import cwd, conf, settings

_log = logging.getLogger(__name__)


class Bot(commands.Bot): 
    def __init__(self) -> None: 
        self.db = Database()
        self.conf = conf

        self.client: Client = None

        self.log_channel = None
        self.emoji = None

        super().__init__(
            command_prefix="!", 
            intents=Intents.all(), 
            reload=True,
        )

    async def log(
        self, 
        *text: str,
        sep: str = " ",
    ) -> None: 
        if not self.log_channel: return 
        await self.log_channel.send(
            sep.join(text),
            allowed_mentions=disnake.AllowedMentions(users=False), 
        )

    async def on_command_error(
        self,
        ctx: commands.Context,
        error: commands.errors.CommandError,
    ) -> None:
        if isinstance(error, commands.errors.CommandNotFound): 
            return 
        else: 
            _log.warning("Root Error", exc_info=error)    

    @commands.Cog.listener(name="on_ready")
    async def on_ready(self): 
        self.log_channel = self.get_channel(self.conf.log_channel_id)
        self.emoji = self.get_emoji(1459664769639383101)
        disnake.Embed.set_default_color(0x242429)

        _log.info("Bot is Ready")


    @commands.register_injection
    async def user_middleware(
        self, 
        inter: disnake.AppCmdInter, 
    ) -> User: 
        return await self.bot.db.create_or_get_user(
            id=inter.author.id, 
            quartz=1, 
        )

    @commands.Cog.listener(name="on_connect") 
    async def on_connect(self): 
        if not self.client: 
            self.client = Client(token=settings.unbelievaboat_key)
 
    @commands.command(name="conf-validate")
    @commands.has_permissions(administrator=True)
    async def conf_validate(self, ctx: commands.Context): 
        self.conf = self.conf.reload()
        await ctx.reply("Конфиг обновлен!")