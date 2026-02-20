# 🔥 Hikka/Heroku Soundpad модуль
# Команда: .sp <название>
# Берёт mp3 с lerman.vercel.app/<название>.mp3 и отправляет как голосовое

from hikka import loader, utils
import os
import aiohttp
from pydub import AudioSegment

@loader.tds
class SoundPadMod(loader.Module):
    """🎵 Soundpad by Lerman"""
    strings = {"name": "SoundPad"}

    async def spcmd(self, message):
        """Использование: .sp <название>"""
        args = utils.get_args(message)
        if not args:
            await message.edit("😏 Лерман, укажи название трека после .sp")
            return
        track_name = args[0]
        mp3_url = f"https://lerman.vercel.app/{track_name}.mp3"
        tmp_mp3 = f"/data/data/com.termux/files/home/Heroku/{track_name}.mp3"
        tmp_ogg = f"/data/data/com.termux/files/home/Heroku/{track_name}.ogg"

        await message.edit(f"🎶 Ловлю трек `{track_name}`...")

        try:
            # Скачиваем mp3
            async with aiohttp.ClientSession() as session:
                async with session.get(mp3_url) as resp:
                    if resp.status != 200:
                        await message.edit("💀 Трек не найден 😭")
                        return
                    data = await resp.read()
                    with open(tmp_mp3, "wb") as f:
                        f.write(data)

            # Конвертируем в ogg для Telegram voice
            audio = AudioSegment.from_mp3(tmp_mp3)
            audio.export(tmp_ogg, format="ogg", codec="libopus")

            # Отправляем как голосовое
            await message.client.send_file(
                message.chat_id,
                tmp_ogg,
                voice_note=True,
                caption=f"🎤 {track_name}"
            )

            await message.delete()
        except Exception as e:
            await message.edit(f"💀 Ошибка: {e}")
        finally:
            # Удаляем временные файлы
            if os.path.exists(tmp_mp3):
                os.remove(tmp_mp3)
            if os.path.exists(tmp_ogg):
                os.remove(tmp_ogg)
