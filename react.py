from .. import loader, utils
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
import asyncio

@loader.tds
class PoopReactorMod(loader.Module):
    """💩 реактор (live + mass attack)"""

    strings = {"name": "PoopReactor"}

    def __init__(self):
        self.chat_id = -1002338569737
        self.enabled = False

    # 🔘 ВКЛ/ВЫКЛ
    async def poopcmd(self, message):
        """вкл/выкл авто 💩"""
        self.enabled = not self.enabled
        status = "включен 💩" if self.enabled else "выключен 🚫"
        await utils.answer(message, f"Режим {status}")

    # 💣 СУПЕР БОМБАРДИРОВКА
    async def poopallcmd(self, message):
        """💩 turbo атака на сообщения"""
        await utils.answer(message, "💩 Запускаю ЖЁСТКИЙ РЕЖИМ... держись 😈")

        messages = []
        async for msg in message.client.iter_messages(self.chat_id, limit=50000):
            messages.append(msg.id)

        workers = 5  # ⚡ можешь увеличить, если хочешь рискнуть

        async def worker(chunk):
            for msg_id in chunk:
                try:
                    await message.client(
                        SendReactionRequest(
                            peer=self.chat_id,
                            msg_id=msg_id,
                            reaction=[ReactionEmoji(emoticon="💩")],
                            big=False
                        )
                    )
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print("ERROR:", e)
                    await asyncio.sleep(1)

        chunks = [messages[i::workers] for i in range(workers)]

        await asyncio.gather(*[worker(chunk) for chunk in chunks])

        await utils.answer(message, "💩 ЧАТ ПРОШЁЛ ЧЕРЕЗ АД.")

    # 👀 ЛАЙВ РЕЖИМ
    async def watcher(self, message):
        if not self.enabled:
            return

        if message.chat_id != self.chat_id:
            return

        try:
            await message.client(
                SendReactionRequest(
                    peer=self.chat_id,
                    msg_id=message.id,
                    reaction=[ReactionEmoji(emoticon="❤️")],
                    big=False
                )
            )
        except:
            pass
