from .. import loader, utils

@loader.tds
class RBSMod(loader.Module):
    """Roleplay Ban System + Karma + Verdict"""

    strings = {"name": "RBS"}

    async def client_ready(self, client, db):
        self.db = db
        self.karma = db.get("RBS", "karma", {})
        self.warns = db.get("RBS", "warns", {})

    def save(self):
        self.db.set("RBS", "karma", self.karma)
        self.db.set("RBS", "warns", self.warns)

    async def rbhelpcmd(self, message):
        """.rbhelp — список команд"""
        text = (
            "⚙️ <b>RBS — система модерации</b>\n\n"
            ".givekarma <число> — изменить карму\n"
            ".warn <причина> — выдать варн\n"
            ".ban <причина> — бан сообщение\n"
            ".court — начать суд\n"
            ".verdict <guilty/innocent> — вынести приговор\n"
            ".who — досье пользователя\n"
        )
        await utils.answer(message, text)

    async def givekarmacmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "⚠️ Укажи число")
        try:
            value = int(args)
        except:
            return await utils.answer(message, "⚠️ Это не число")

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение пользователя")

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
        reason = utils.get_args_raw(message) or "не указана"
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение пользователя")

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
        reason = utils.get_args_raw(message) or "не указана"
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение пользователя")

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

    async def courtcmd(self, message):
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение подсудимого")

        judge = await message.get_sender()
        target = await reply.get_sender()

        judge_link = f'<a href="tg://user?id={judge.id}">{judge.first_name}</a>'
        target_link = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

        text = (
            f"⚖️ <b>Суд начался</b>\n\n"
            f"👨‍⚖️ Судья: {judge_link}\n"
            f"🧑 Подсудимый: {target_link}\n\n"
            f"Ожидается приговор..."
        )
        await reply.reply(text)

    async def whocmd(self, message):
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение пользователя")

        target = await reply.get_sender()
        uid = str(target.id)

        karma = self.karma.get(uid, 0)
        warns = self.warns.get(uid, 0)

        target_link = f'<a href="tg://user?id={target.id}">{target.first_name}</a>'

        text = (
            f"🕵️ <b>Досье пользователя</b>\n\n"
            f"👤 Пользователь: {target_link}\n"
            f"⭐ Карма: <b>{karma}</b>\n"
            f"⚠️ Варны: <b>{warns}/2</b>"
        )
        await reply.reply(text)

    async def verdictcmd(self, message):
        args = utils.get_args_raw(message).lower()
        if not args:
            return await utils.answer(message, "⚠️ Укажи приговор: guilty или innocent")

        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "⚠️ Ответь на сообщение суда (.court)")

        target_name = "подсудимый"
        try:
            lines = reply.text.split("\n")
            for line in lines:
                if "Подсудимый:" in line:
                    target_name = line.split("Подсудимый:")[1].strip()
                    break
        except:
            pass

        judge = await message.get_sender()
        judge_link = f'<a href="tg://user?id={judge.id}">{judge.first_name}</a>'

        if args == "guilty":
            verdict_text = f"🔨 Приговор: ВИНОВЕН\n👨‍⚖️ Судья: {judge_link}\n⚠️ Последствия могут быть назначены"
        elif args == "innocent":
            verdict_text = f"✅ Приговор: НЕ ВИНОВЕН\n👨‍⚖️ Судья: {judge_link}\n🎉 Подсудимый {target_name} свободен"
        else:
            return await utils.answer(message, "⚠️ Неверный аргумент. Используй guilty или innocent")

        await reply.reply(verdict_text)
