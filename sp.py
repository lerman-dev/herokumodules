import os
import aiohttp
from hikka import loader, utils
from telethon.tl.types import InputMediaUploadedAudio
from pathlib import Path

@loader.tds
class SoundpadMod(loader.Module):
    """🎤 Soundpad с кешем Лермана"""
    strings = {"name": "Soundpad"}
    
    def __init__(self):
        self.cache_dir = Path(os.getenv("HOME") + "/downloads/sp_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)  # создаём папку если нет

    async def spcmd(self, message):
        """Использование: .sp <трек>"""
        args = utils.get_args(message)
        if not args:
            await message.edit("💀 Укажи название трека")
            return

        track_name = args[0]
        mp3_path = self.cache_dir / f"{track_name}.mp3"

        # 🔹 Если файл есть — не скачиваем
        if not mp3_path.exists():
            url = f"https://lerman.vercel.app/{track_name}.mp3"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            await message.edit(f"💀 Ошибка скачивания: {resp.status}")
                            return
                        data = await resp.read()
                        mp3_path.write_bytes(data)
            except Exception as e:
                await message.edit(f"💀 Ошибка: {e}")
                return

        # 🔹 Отправка в чат без удаления
        await message.client.send_file(message.chat_id, mp3_path, voice_note=True)
        await message.delete()  # чтобы чат не засорять командой
