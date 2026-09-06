import disnake 
from functools import wraps 
from utils.types import Callback


def callback_data_injection(): 
    def decorator(func):
        @wraps(func)
        async def wrapper(self, inter: disnake.MessageInteraction):
            data = inter.data.custom_id.split(":")
            callback = Callback(
                custom_id=data[0], 
                author_id=(int(data[1]) if len(data) > 1 else None), 
                character_id=(int(data[2]) if len(data) > 2 else None)
            )
            return await func(self, inter, callback)
        return wrapper
    return decorator


def custom_id_check(custom_id: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, inter: disnake.MessageInteraction):
            if not inter.data.custom_id.startswith(custom_id):
                return
            return await func(self, inter)
        return wrapper
    return decorator