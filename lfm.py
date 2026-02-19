from .. import loader, utils
import requests

class LFMMod(loader.Module):
    """Показывает текущий трек из Last.fm"""

    strings = {"name": "LFM"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                "Last.fm API ключ",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "username",
                "lermandev",
                "Last.fm username",
                validator=loader.validators.String()
            )
        )

    @loader.ratelimit
    async def lfmcmd(self, message):
        """Показать текущий трек"""
        api_key = self.config["api_key"]
        user = self.config["username"]

        if not api_key:
            await utils.answer(message, "❌ Вставь API ключ через конфиг")
            return

        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.getrecenttracks",
            "user": user,
            "api_key": api_key,
            "format": "json",
            "limit": 1
        }

        try:
            r = requests.get(url, params=params).json()
            track = r["recenttracks"]["track"][0]

            name = track["name"]
            artist = track["artist"]["#text"]

            now_playing = track.get("@attr", {}).get("nowplaying")

            if now_playing:
                text = f"🎧 Сейчас играет:\n<b>{artist} — {name}</b>"
            else:
                text = f"🕓 Последний трек:\n<b>{artist} — {name}</b>"

            await utils.answer(message, text)

        except Exception as e:
            await utils.answer(message, f"❌ Ошибка:\n<code>{e}</code>")
