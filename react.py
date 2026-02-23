from .. import loader, utils
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji
import asyncio

@loader.tds
class PoopReactorMod(loader.Module):
    """💩 реактор с массовым режимом"""

    strings = {"name": "PoopReactor"}

    def __init__(self):
        self.chat_id = -1002338569737
        self.enabled = False

    async def poopcmd(self, message):
        """вкл/выкл авто 💩"""
        self.enabled = not self.enabled
        status = "включен 💩" if self.enabled else "выключен 🚫"
        await utils.answer(message, f"Режим {status}")

    async def poopallcmd(self, message):
        """💩 на ВСЕ сообщения"""
        await utils.answer(message, "Начинаю 💩-геноцид... держись 😈")

        async for msg in message.client.iter_messages(self.chat_id):
            try:
                await message.client(
                    SendReactionRequest(
                        peer=self.chat_id,
                        msg_id=msg.id,
                        reaction=[ReactionEmoji(emoticon="💩")],
                        big=False
                    )
                )
                await asyncio.sleep(0.5)  # анти-бан пауза
            except:
                await asyncio.sleep(1)

        await utils.answer(message, "💩 Готово. Чат официально испорчен.")

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
                    reaction=[ReactionEmoji(emoticon="💩")],
                    big=False
                )
            )
        except:
            pass
