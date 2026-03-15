from .. import loader, utils

@loader.tds
class KarmaBanMod(loader.Module):
    """Карма и фейк бан"""

    strings = {"name": "KarmaBan"}

    async def givekarmacmd(self, message):
        """.givekarma <число> (ответом на сообщение)"""

        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, "🤨 Напиши число кармы")

        try:
            value = int(args)
        except:
            return await utils.answer(message, "🤨 Это не число")

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение пользователя")

        giver = await message.get_sender()
        target = await reply.get_sender()

        giver_link = f'<a href="tg://user?id={giver.id}">{giver.first_name}</a>'
        target_link = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

        text = (
            f"🔰 {giver_link} изменил карму на <b>{value}</b> пользователю {target_link}\n"
            f"🔰 Новое значение кармы: <b>{value}</b>"
        )

        await reply.reply(text)

    async def bancmd(self, message):
        """.ban <причина> (ответом на сообщение)"""

        reason = utils.get_args_raw(message) or "не указана"

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение нарушителя")

        admin = await message.get_sender()
        target = await reply.get_sender()

        admin_link = f'<a href="tg://user?id={admin.id}">{admin.first_name}</a>'
        target_link = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

        text = (
            f"🚫 {target_link} получил(а) бан навсегда\n"
            f"👮 Администратор: {admin_link}\n"
            f"📝 Причина: <b>{reason}</b>"
        )

        await reply.reply(text)
