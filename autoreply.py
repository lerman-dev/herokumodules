from hikka import loader, utils
from datetime import datetime, time as dtime
import pytz

@loader.tds
class AutoReplyMod(loader.Module):
    """💤 AutoReply Лермана"""
    strings = {"name": "AutoReply"}

    def __init__(self):
        self.enabled = False
        self.always_on = False

    async def autoreplycmd(self, message):
        args = utils.get_args(message)
        if not args:
            await message.edit("😏 on / off / always")
            return

        mode = args[0].lower()

        if mode == "on":
            self.enabled = True
            self.always_on = False
            await message.edit("🌙 Ночной режим включён (днём АБСОЛЮТНАЯ ТИШИНА 💀)")
        elif mode == "off":
            self.enabled = False
            self.always_on = False
            await message.edit("💤 Выключено")
        elif mode == "always":
            self.enabled = True
            self.always_on = True
            await message.edit("🔥 Всегда отвечает (опасный вайб 💀)")
        else:
            await message.edit("💀 on / off / always")

    async def watcher(self, message):
        if not self.enabled:
            return

        text = message.raw_text.lower()
        if not any(x in text for x in ["@lermandev", "лерман"]):
            return

        tz = pytz.timezone("Asia/Almaty")
        now = datetime.now(tz).time()

        sleep_start = dtime(1, 30)
        sleep_end = dtime(12, 30)

        # 🔥 ALWAYS — отвечает ВСЕГДА
        if self.always_on:
            await message.reply("😴 Возможно, я сплю, с ~12:30 GMT+6 возможно проснусь")
            return

        # 💀 ON — ТОЛЬКО НОЧЬ
        is_night = (now >= sleep_start) or (now <= sleep_end)

        if not is_night:
            return  # ← ВОТ ОНО. ДНЁМ НИЧЕГО НЕ ДЕЛАЕТ 😎

        await message.reply("😴 Возможно, я сплю, с ~12:30 GMT+6 возможно проснусь")
