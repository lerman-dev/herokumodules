from .. import loader, utils
import asyncio
from datetime import datetime, timedelta

@loader.tds
class LermanTimeMod(loader.Module):
    """Меняет имя на Lerman | время (GMT+6)"""

    strings = {"name": "LermanTime"}

    async def client_ready(self, client, db):
        self._client = client
        self._running = True
        asyncio.create_task(self._loop())

    async def _loop(self):
        while self._running:
            try:
                # текущее время +6 часов
                now = datetime.utcnow() + timedelta(hours=6)
                time_str = now.strftime("%H:%M")

                new_name = f"Lerman | {time_str}"

                await self._client(functions.account.UpdateProfileRequest(
                    first_name=new_name
                ))

            except Exception as e:
                print("Ошибка:", e)

            await asyncio.sleep(60)

    async def unload(self):
        self._running = False
