import os 
import sys
import logging 

from bot import Bot
from settings import settings, cwd
from utils.logging import setup_logging


setup_logging()

bot = Bot()
_log = logging.getLogger()
bot.i18n.load(cwd / "json" / "locales")


for directory, directories, files in os.walk("./core"):
    for file in os.listdir(directory):
        if file.endswith(".py") and not file.startswith("_"):
            try:
                module_name = os.path.splitext(os.path.relpath(os.path.join(directory, file), "."))[0]
                module_name = module_name.replace(os.sep, ".")
                bot.load_extension(module_name)
                _log.info(f"Cog {file[:-3]} loaded")
            except Exception as e:
                _log.exception("Error on cogs loading")  


if __name__ == '__main__':
    if not settings.token: 
        raise ValueError("Bot token not provided")
    
    try:  
        bot.run(settings.token)
    except KeyboardInterrupt: 
        _log.info("Bot stopped from developer")
    except Exception: 
        _log.exception("Root Error")
    finally: 
        sys.exit(0) 