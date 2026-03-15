from .. import loader, utils

@loader.tds
class KarmaMod(loader.Module):
    """Изменение кармы"""

    strings = {"name": "KarmaMod"}

    async def givekarmacmd(self, message):
        """Использование: .givekarma <число> (ответом на сообщение)"""

        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, "🤨 Напиши число кармы")

        try:
            value = int(args)
        except:
            return await utils.answer(message, "🤨 Это не число")

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Команда должна быть ответом на сообщение")

        giver = await message.get_sender()
        target = await reply.get_sender()

        giver_name = giver.first_name
        target_name = target.first_name

        giver_link = f'<a href="tg://user?id={giver.id}">{giver_name}</a>'
        target_link = f'<a href="tg://user?id={target.id}">{target_name}</a>'

        text = (
            f"🔰 {giver_link} изменил карму на <b>{value}</b> пользователю {target_link}\n"
            f"🔰 Новое значение кармы: <b>{value}</b>"
        )

        await utils.answer(message, text)
