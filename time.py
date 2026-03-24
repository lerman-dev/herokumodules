# -*- coding: utf-8 -*-
import os
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, get_text

filename = os.path.basename(__file__)
Module_Name = 'LermanTime'

LANGUAGES = {
    "en": {
        "started": "🚀 <b>Started, time is ticking</b>",
        "already_running": "⚡ <b>Already running, don't click like crazy</b>",
        "stopped": "🛑 <b>Timer stopped</b>",
        "usage": "📌 <b>Usage:</b> <code>.lerman start / stop</code>"
    },
    "ru": {
        "started": "🚀 <b>Запустил, время пошло тикать</b>",
        "already_running": "⚡ <b>Уже крутится, не жми как бешеный</b>",
        "stopped": "🛑 <b>Всё, таймер умер</b>",
        "usage": "📌 <b>Использование:</b> <code>.lerman start / stop</code>"
    },
    "ua": {
        "started": "🚀 <b>Запустив, час пішов цокати</b>",
        "already_running": "⚡ <b>Вже крутиться, не тисни як шалений</b>",
        "stopped": "🛑 <b>Все, таймер помер</b>",
        "usage": "📌 <b>Використання:</b> <code>.lerman start / stop</code>"
    }
}

# Глобальная переменная для отслеживания состояния
running = False


@Client.on_message(fox_command("lerman", Module_Name, filename, "[start/stop]") & fox_sudo())
async def lerman_cmd(client, message):
    global running
    message = await who_message(client, message)
    
    args = message.text.split()
    cmd = args[1] if len(args) > 1 else ""
    
    if cmd == "start":
        if not running:
            running = True
            asyncio.create_task(loop(client))
            text = get_text("lerman", "started", LANGUAGES=LANGUAGES)
            await message.edit(text)
        else:
            text = get_text("lerman", "already_running", LANGUAGES=LANGUAGES)
            await message.edit(text)
    
    elif cmd == "stop":
        running = False
        text = get_text("lerman", "stopped", LANGUAGES=LANGUAGES)
        await message.edit(text)
    
    else:
        text = get_text("lerman", "usage", LANGUAGES=LANGUAGES)
        await message.edit(text)


async def loop(client):
    """Основной цикл обновления имени"""
    global running
    
    while running:
        try:
            # Получаем текущее время (UTC+6)
            t = (datetime.utcnow() + timedelta(hours=6)).strftime("%H:%M")
            new_name = f"Lerman | {t}"
            
            # Обновляем имя профиля
            await client.update_profile(first_name=new_name)
            
        except Exception as e:
            print(f"Ошибка при обновлении имени: {e}")
        
        # Ждём 60 секунд перед следующим обновлением
        await asyncio.sleep(60)
