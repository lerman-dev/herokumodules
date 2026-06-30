from .. import loader, utils
import asyncio
from datetime import datetime, timedelta
from telethon.tl.functions.account import UpdateProfileRequest

@loader.tds
class LermanTime(loader.Module):
    """Lerman | время в нике"""

    strings = {"name": "LermanTime"}

    async def client_ready(self, client, db):
        self.client = client
        self.running = False

    async def lermancmd(self, message):
        args = utils.get_args_raw(message)

        if args == "start":
            if not self.running:
                self.running = True
                asyncio.create_task(self.loop())
                await utils.answer(message, "🚀 Запустил, время пошло тикать")
            else:
                await utils.answer(message, "⚡ Уже крутится, не жми как бешеный")

        elif args == "stop":
            self.running = False
            await utils.answer(message, "🛑 Всё, таймер умер")

        else:
            await utils.answer(message, "Используй: .lerman start / stop")

    async def loop(self):
        while self.running:
            try:
                t = (datetime.utcnow() + timedelta(hours=6)).strftime("%H:%M")
                await self.client(UpdateProfileRequest(
                    first_name=f"/home/lerman | {t}"
                ))
            except Exception as e:
                print("Ошибка:", e)

            await asyncio.sleep(60)
