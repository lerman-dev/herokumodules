from .. import loader, utils
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

@loader.tds
class PoopReactorMod(loader.Module):
    """Ставит 💩 по команде"""

    strings = {"name": "PoopReactor"}

    def __init__(self):
        self.chat_id = -1002338569737
        self.enabled = False

    async def poopcmd(self, message):
        """вкл/выкл 💩 режим"""
        self.enabled = not self.enabled

        status = "включен 💩" if self.enabled else "выключен 🚫"
        await utils.answer(message, f"Режим {status}")

    async def watcher(self, message):
        if not self.enabled:
            return

        if not message or not message.chat_id:
            return

        if message.chat_id != self.chat_id:
            return

        try:
            await message.client(
                SendReactionRequest(
                    peer=message.chat_id,
                    msg_id=message.id,
                    reaction=[ReactionEmoji(emoticon="💩")],
                    big=False
                )
            )
        except:
            pass
