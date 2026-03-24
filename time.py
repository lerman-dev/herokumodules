# -*- coding: utf-8 -*-
import os
import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message, get_text

# Настройка логирования
logger = logging.getLogger(__name__)

filename = os.path.basename(__file__)
Module_Name = 'LermanTime'

LANGUAGES = {
    "en": {
        "started": "🚀 <b>Started, time is ticking</b>\n⏰ <b>Name will update every minute</b>",
        "already_running": "⚡ <b>Already running, don't click like crazy</b>",
        "stopped": "🛑 <b>Timer stopped</b>",
        "usage": "📌 <b>Usage:</b> <code>.lerman start / stop</code>",
        "update_success": "🔄 <b>Name updated:</b> <code>{name}</code>",
        "update_error": "❌ <b>Error updating name:</b> <code>{error}</code>"
    },
    "ru": {
        "started": "🚀 <b>Запустил, время пошло тикать</b>\n⏰ <b>Имя будет обновляться каждую минуту</b>",
        "already_running": "⚡ <b>Уже крутится, не жми как бешеный</b>",
        "stopped": "🛑 <b>Всё, таймер умер</b>",
        "usage": "📌 <b>Использование:</b> <code>.lerman start / stop</code>",
        "update_success": "🔄 <b>Имя обновлено:</b> <code>{name}</code>",
        "update_error": "❌ <b>Ошибка обновления имени:</b> <code>{error}</code>"
    },
    "ua": {
        "started": "🚀 <b>Запустив, час пішов цокати</b>\n⏰ <b>Ім'я буде оновлюватись щохвилини</b>",
        "already_running": "⚡ <b>Вже крутиться, не тисни як шалений</b>",
        "stopped": "🛑 <b>Все, таймер помер</b>",
        "usage": "📌 <b>Використання:</b> <code>.lerman start / stop</code>",
        "update_success": "🔄 <b>Ім'я оновлено:</b> <code>{name}</code>",
        "update_error": "❌ <b>Помилка оновлення імені:</b> <code>{error}</code>"
    }
}

# Глобальная переменная для отслеживания состояния
running = False
update_task = None


@Client.on_message(fox_command("lerman", Module_Name, filename, "[start/stop]") & fox_sudo())
async def lerman_cmd(client, message):
    global running, update_task
    message = await who_message(client, message)
    
    args = message.text.split()
    cmd = args[1] if len(args) > 1 else ""
    
    if cmd == "start":
        if not running:
            running = True
            # Запускаем задачу в фоне
            update_task = asyncio.create_task(update_name_loop(client, message.chat.id))
            text = get_text("lerman", "started", LANGUAGES=LANGUAGES)
            await message.edit(text)
            logger.info("LermanTime started")
        else:
            text = get_text("lerman", "already_running", LANGUAGES=LANGUAGES)
            await message.edit(text)
    
    elif cmd == "stop":
        running = False
        if update_task:
            update_task.cancel()
            update_task = None
        text = get_text("lerman", "stopped", LANGUAGES=LANGUAGES)
        await message.edit(text)
        logger.info("LermanTime stopped")
    
    else:
        text = get_text("lerman", "usage", LANGUAGES=LANGUAGES)
        await message.edit(text)


async def update_name_loop(client, chat_id=None):
    """Основной цикл обновления имени с логированием"""
    global running
    
    logger.info("Starting name update loop")
    
    while running:
        try:
            # Получаем текущее время (UTC+6)
            current_time = datetime.utcnow() + timedelta(hours=6)
            t = current_time.strftime("%H:%M")
            new_name = f"Lerman | {t}"
            
            # Обновляем имя профиля
            await client.update_profile(first_name=new_name)
            
            # Логируем успешное обновление
            logger.info(f"Name updated to: {new_name}")
            
            # Отправляем сообщение о обновлении (если указан chat_id)
            if chat_id:
                try:
                    text = get_text("lerman", "update_success", LANGUAGES=LANGUAGES, name=new_name)
                    await client.send_message(chat_id, text)
                except Exception as e:
                    logger.error(f"Failed to send update message: {e}")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error updating name: {error_msg}")
            
            # Отправляем сообщение об ошибке (если указан chat_id)
            if chat_id:
                try:
                    text = get_text("lerman", "update_error", LANGUAGES=LANGUAGES, error=error_msg)
                    await client.send_message(chat_id, text)
                except Exception as e:
                    logger.error(f"Failed to send error message: {e}")
        
        # Ждём 60 секунд перед следующим обновлением
        await asyncio.sleep(60)
    
    logger.info("Name update loop stopped")


# Добавляем обработчик для остановки при завершении
async def cleanup():
    """Очистка при завершении"""
    global running, update_task
    if running:
        running = False
        if update_task:
            update_task.cancel()
            logger.info("Cleanup: stopped LermanTime")
