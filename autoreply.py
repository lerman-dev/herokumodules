# 🔥 Hikka/Heroku AutoReply модуль с постоянным ответчиком
from hikka import loader, utils
from datetime import datetime, time as dtime
import pytz  # pip install pytz

@loader.tds
class AutoReplyMod(loader.Module):
    """💤 AutoReply Лермана с командой включения/выключения и постоянным режимом"""
    strings = {"name": "AutoReply"}

    def __init__(self):
        self.enabled = True       # обычный режим включен
        self.always_on = False    # постоянный ответчик

    async def autoreplycmd(self, message):
        """Использование: .autoreply on/off/always"""
        args = utils.get_args(message)
        if not args:
            await message.edit("😏 Лерман, укажи 'on', 'off' или 'always'")
            return

        mode = args[0].lower()
        if mode == "on":
            self.enabled = True
            self.always_on = False
            await message.edit("✅ AutoReply включён (ночной сон учтён) 😎")
        elif mode == "off":
            self.enabled = False
            self.always_on = False
            await message.edit("💤 AutoReply выключен 😏")
        elif mode == "always":
            self.enabled = True
            self.always_on = True
            await message.edit("🔥 AutoReply включён всегда, вайб 24/7 😎💀")
        else:
            await message.edit("💀 Неправильный аргумент, используй 'on', 'off' или 'always'")

    async def watcher(self, message):
        if not self.enabled:
            return  # Если выключен — не реагируем

        text = message.raw_text.lower()
        mentions = ["@lermandev", "лерман"]

        if not any(x in text for x in mentions):
            return

        # GMT+6
        tz = pytz.timezone("Asia/Almaty")
        now = datetime.now(tz).time()

        # Сон с 1:30 до 12:30
        sleep_start = dtime(1, 30)
        sleep_end = dtime(12, 30)

        if self.always_on:
            # Игнорируем время — отвечаем всегда
            await message.reply("😎 Лерман на связи, всегда на вайбе!")
        elif now >= sleep_start or now <= sleep_end:
            await message.reply("😴 Возможно, я сплю, с ~12:30 GMT+6 возможно проснусь")
        # Иначе — ничего, дневной режим, вайб активен но спим не надо
