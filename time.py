from .. import loader, utils
import asyncio
from datetime import datetime, timedelta
from telethon.tl import functions

@loader.tds
class LermanTimeMod(loader.Module):
    """Меняет имя на Lerman | время (GMT+6) по команде"""

    strings = {"name": "LermanTime"}
    
    async def client_ready(self, client, db):
        self._client = client
        self._running = False  # не стартуем сразу
        self._task = None

    async def lermancmd(self, message):
        """Команда: .lerman start/stop"""
        args = utils.get_args_raw(message).lower()
        
        if args == "start":
            if not self._running:
                self._running = True
                self._task = asyncio.create_task(self._loop())
                await utils.answer(message, "🚀 LermanTime запущен!")
            else:
                await utils.answer(message, "⚡ Уже запущено")
        elif args == "stop":
            if self._running:
                self._running = False
                await utils.answer(message, "🛑 LermanTime остановлен")
            else:
                await utils.answer(message, "⚡ Уже остановлено")
        else:
            await utils.answer(message, "Используй: .lerman start / stop")

    async def _loop(self):
        while self._running:
            try:
                now = datetime.utcnow() + timedelta(hours=6)
                time_str = now.strftime("%H:%M")
                new_name = f"Lerman | {time_str}"

                await self._client(functions.account.UpdateProfileRequest(
                    first_name=new_name
                ))
            except Exception as e:
                print("Ошибка:", e)

            await asyncio.sleep(60)  # меняем каждые 60 секунд
