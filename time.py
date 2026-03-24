# -*- coding: utf-8 -*-
import os
import asyncio
from datetime import datetime, timedelta
from pyrogram import Client, filters
from command import fox_command, fox_sudo, who_message

filename = os.path.basename(__file__)
Module_Name = 'LermanTime'

TRIGGER_FILE = "triggers/lerman_active"

@Client.on_message(fox_command("lerman", Module_Name, filename, "[start/stop]") & fox_sudo())
async def lerman_cmd(client, message):
    message = await who_message(client, message)
    
    args = message.text.split()
    cmd = args[1] if len(args) > 1 else ""
    
    if cmd == "start":
        # Создаём файл-триггер
        with open(TRIGGER_FILE, "w", encoding="utf-8") as f:
            f.write("lerman_worker")
        await message.edit("🚀 <b>Запущено! Бот будет обновлять имя</b>")
        
    elif cmd == "stop":
        # Удаляем файл-триггер
        if os.path.exists(TRIGGER_FILE):
            os.remove(TRIGGER_FILE)
        await message.edit("🛑 <b>Остановлено</b>")
        
    else:
        await message.edit("📌 <b>Использование:</b> <code>.lerman start</code> или <code>.lerman stop</code>")


# ЭТА ФУНКЦИЯ БУДЕТ ВЫПОЛНЯТЬСЯ ПРИ ЗАПУСКЕ БОТА
# Просто вставьте этот код в конец файла, он будет работать
# независимо от команды
import threading
import time

def name_updater():
    while True:
        try:
            # Проверяем, запущен ли модуль
            if os.path.exists(TRIGGER_FILE):
                # Импортируем клиент глобально
                from main import app
                t = (datetime.utcnow() + timedelta(hours=6)).strftime("%H:%M")
                new_name = f"Lerman | {t}"
                
                # Обновляем имя
                async def update():
                    try:
                        await app.update_profile(first_name=new_name)
                        print(f"[Lerman] Updated: {new_name}")
                    except Exception as e:
                        print(f"[Lerman] Error: {e}")
                
                # Запускаем обновление
                loop = asyncio.new_event_loop()
                loop.run_until_complete(update())
                loop.close()
        except Exception as e:
            print(f"[Lerman] Loop error: {e}")
        
        time.sleep(60)

# Запускаем поток при загрузке модуля
thread = threading.Thread(target=name_updater, daemon=True)
thread.start()
print("[Lerman] Module loaded, thread started")
