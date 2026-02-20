# 🎤 Soundpad модуль Лермана с кешем для Hikka/Heroku
import os
import aiohttp
from hikka import loader, utils
from pathlib import Path

@loader.tds
class SoundpadMod(loader.Module):
    """🎵 Soundpad с кешированием Лермана"""
    strings = {"name": "Soundpad"}

    def __init__(self):
        # Директория для кеша
        self.cache_dir = Path(os.getenv("HOME") + "/downloads/sp_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def spcmd(self, message):
        """Использование: .sp <название трека>"""
        args = utils.get_args(message)
        if not args:
            await message.edit("💀 Укажи название трека, унитаз 😏")
            return

        track_name = args[0]
        mp3_path = self.cache_dir / f"{track_name}.mp3"

        # 🔹 Если трек ещё не скачан — качаем
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

        # 🔹 Отправка в чат как голосовое сообщение
        try:
            await message.client.send_file(message.chat_id, mp3_path, voice_note=True)
            await message.delete()  # чтобы чат не засорять командой
        except Exception as e:
            await message.edit(f"💀 Ошибка при отправке: {e}")
