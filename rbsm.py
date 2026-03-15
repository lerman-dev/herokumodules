from .. import loader, utils

@loader.tds
class KarmaWarnMod(loader.Module):
    """Карма + warn система"""

    strings = {"name": "KarmaWarn"}

    async def client_ready(self, client, db):
        self.db = db
        self.karma = db.get("KarmaWarn", "karma", {})
        self.warns = db.get("KarmaWarn", "warns", {})

    def save(self):
        self.db.set("KarmaWarn", "karma", self.karma)
        self.db.set("KarmaWarn", "warns", self.warns)

    async def givekarmacmd(self, message):
        """.givekarma <число> (ответом)"""

        args = utils.get_args_raw(message)

        if not args:
            return await utils.answer(message, "🤨 Укажи число")

        try:
            value = int(args)
        except:
            return await utils.answer(message, "🤨 Это не число")

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение")

        giver = await message.get_sender()
        target = await reply.get_sender()

        uid = str(target.id)

        current = self.karma.get(uid, 0)
        current += value
        self.karma[uid] = current

        self.save()

        giver_link = f'<a href="tg://user?id={giver.id}">{giver.first_name}</a>'
        target_link = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

        text = (
            f"🔰 {giver_link} изменил карму на <b>{value}</b> пользователю {target_link}\n"
            f"🔰 Новое значение кармы: <b>{current}</b>"
        )

        await reply.reply(text)

    async def warncmd(self, message):
        """.warn <причина> (ответом)"""

        reason = utils.get_args_raw(message) or "не указана"

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение")

        admin = await message.get_sender()
        target = await reply.get_sender()

        uid = str(target.id)

        warns = self.warns.get(uid, 0) + 1
        self.warns[uid] = warns

        self.save()

        admin_link = f'<a href="tg://user?id={admin.id}">{admin.first_name}</a>'
        target_link = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

        if warns >= 2:
            text = (
                f"🚫 {target_link} получил(а) бан навсегда\n"
                f"👮 Администратор: {admin_link}\n"
                f"📝 Причина: 2 варна"
            )

            self.warns[uid] = 0
            self.save()

        else:
            text = (
                f"❗️ {target_link} получил(а) варн ({warns}/2)\n"
                f"👮 Администратор: {admin_link}\n"
                f"📝 Причина: <b>{reason}</b>"
            )

        await reply.reply(text)

    async def bancmd(self, message):
        """.ban <причина>"""

        reason = utils.get_args_raw(message) or "не указана"

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение")

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
