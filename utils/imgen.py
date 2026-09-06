"""Image generator functions"""
import io 
import disnake 
import aiohttp

from PIL import Image
from db.models import CharacterSlot

from settings import cwd
from typing import List

headers = {"User-Agent": "Mozilla/5.0"}

_images_path = cwd / "media/banners"
_backgrounds_path = cwd / "media/backgrounds"
_total_banners = len(list(_backgrounds_path.iterdir()))
_character_slots_xy = {
    0: (99, 45), 
    1: (307, 45), 
    2: (515, 45), 
}

async def _img_from_url(url) -> bytes:  
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response: 
            if response.status == 200: 
                return await response.read()


async def characters_image_generate(
    characters: List[CharacterSlot],
    banner_id: int = 1, 
) -> disnake.File: 
    banner_path = _images_path / f"characters_banner_{banner_id}.png"
    img = Image.open(banner_path).convert("RGBA")

    for c in characters:
        if not c.character_id: continue

        xy = _character_slots_xy[c.index]
        if not xy: continue
    
        icon = await _img_from_url(c.image_url)
        if not icon: continue 

        cimg = Image.open(io.BytesIO(icon)).convert("RGBA")
        cimg = cimg.resize((120, 214))
        
        img.paste(cimg, xy, cimg)

    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    return disnake.File(buffer, "characters_banner.png")
