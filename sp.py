__dependencies__ = ["aiohttp>=3.8.1", "telethon>=2.25.0", "pytz>=2023.3"]

import os
import aiohttp
from hikka import loader, utils
from pathlib import Path

@loader.tds
class SoundpadFastMod(loader.Module):
    """🎤 Soundpad Лермана с кешем, ускоренной отправкой и автоудалением команды"""
    strings = {"name": "Soundpad"}

    def __init__(self):
        # Директория для кеша
        self.cache_dir = Path(os.getenv("HOME") + "/downloads/sp_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    async def spcmd(self, message):
        """Использование: .sp <трек>"""
        args = utils.get_args(message)
        if not args:
            await message.edit("💀 Укажи название трека, унитаз 😏")
            return

        track_name = args[0]
        mp3_path = self.cache_dir / f"{track_name}.mp3"

        # 🔹 Скачиваем только если ещё нет
        if not mp3_path.exists():
            url = f"https://lerman.vercel.app/{track_name}.mp3"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status != 200:
                            await message.edit(f"💀 Ошибка скачивания: {resp.status}")
                            return
                        # Читаем поток напрямую в файл для ускорения
                        with open(mp3_path, "wb") as f:
                            while True:
                                chunk = await resp.content.read(1024*16)
                                if not chunk:
                                    break
                                f.write(chunk)
            except Exception as e:
                await message.edit(f"💀 Ошибка: {e}")
                return

        # 🔹 Отправка как голосовое сообщение
        try:
            # Отправка сразу без задержек
            await message.client.send_file(message.chat_id, mp3_path, voice_note=True)
            # 💀 Удаляем команду сразу после отправки
            await message.delete()
        except Exception as e:
            await message.edit(f"💀 Ошибка при отправке: {e}")
