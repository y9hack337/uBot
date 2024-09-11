from pyrogram import Client, filters, idle
from pyrogram.enums import ParseMode
import importlib
from datetime import datetime, timedelta
import time, random
import configparser, asyncio
import os, sys, subprocess
import signal, requests
from meval import meval

os.makedirs("modules", exist_ok=True)

if not os.path.exists("userbot.cfg"):
    config = configparser.ConfigParser()
    config['HACK337_USERBOT'] = {
        'api_id': 'YOUR_API_ID',
        'api_hash': 'YOUR_API_HASH',
        'prefix_userbot': '.,ю'
    }
    with open('userbot.cfg', 'w', encoding = "utf-8") as configfile:
        config.write(configfile)
    print("Создан файл 'userbot.cfg'. Заполните конфиг!")
    exit()

config = configparser.ConfigParser()
config.read('userbot.cfg', "utf-8")

api_id = int(config['HACK337_USERBOT']['api_id'])
api_hash = config['HACK337_USERBOT']['api_hash']
prefix_userbot = config['HACK337_USERBOT']['prefix_userbot'].split(',')

app = Client("my_account2", api_id=api_id, api_hash=api_hash)
start_time = time.time()

message_id, chat_id, time_int, success, fail = None, None, None, 0, 0

cats = [ "≽^•⩊•^≼", "ᓚ₍ ^. .^₎", "ฅ^•ﻌ•^ฅ" ]

processes = {}

info_media = {"type": "photo", "file_id": "https://i.imgur.com/jR5ABCc.png"}

def load_modules():
    modules = []
    amount_modules = 0
    sys.path.append(os.path.abspath("modules"))
    for f in os.listdir("modules"):
        if f.endswith(".py"):
            module_name = f[:-3]
            try:
                module = importlib.import_module(module_name)
                for command in module.commands:
                    modules.append((command['cicon'] ,command['cinfo'], command['ccomand']))
                amount_modules+=1
            except Exception as e:
                print(f"Failed to read module {module_name} info: {e}")
    return modules, amount_modules

def install_package(package_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def restart_script(m_id, chat_id):
    current_time = int(time.time())
    python = sys.executable
    os.execl(
        python,
        python,
        *sys.argv,
        "--message_id",
        str(m_id),
        "--chat_id",
        str(chat_id),
        "--time",
        str(current_time),
    )


@app.on_message(filters.me & filters.command(["help", "хелп", "рудз"], prefixes=prefix_userbot))
async def help_command(client, message):
    await message.delete()
    modules, amount_modules = load_modules()
    prefix = prefix_userbot[0]
    help_text = "**Модулей загружено: {}**\n".format(amount_modules)
    for cicon, cinfo, ccomand in modules:
        help_text += f"{cicon}`{prefix}{cinfo}` - {ccomand}\n"
    help_text += (f"**Стандартные команды:**\n"
                  f"ℹ`{prefix}info` - инфо о юзерботе\n"
                  f"⌛`{prefix}ping` - Пишет пинг\n"
                  f"🔄`{prefix}restart` - Перезапуск юзербота\n"
                  f"📟`{prefix}e` - Выполнение кода\n"
                  f"⌨️`{prefix}t` - Запустить команду в системе\n"
                  f"⛔`{prefix}kill` - Ответьте на сообщение, чтобы убить процесс\n"
                  f"🆕`{prefix}update` - Обновить юзербот\n"
                  f"📥`{prefix}lm` - Установить модуль\n"
                  f"🗑️`{prefix}ulm` - Удалить модуль\n"
                 )
    await message.reply_text(help_text)


@app.on_message(filters.me & filters.command(["info","инфо","штащ"], prefixes=prefix_userbot))
async def info_command(_, message):
    global info_media
    if len(message.text.split(" ")) == 2 and message.reply_to_message:
        repl = message.reply_to_message
        if repl.photo:
            if repl.photo:
                file_id = repl.photo.file_id
                info_media = {"type": "photo", "file_id": file_id}
        elif repl.animation:
            file_id = repl.animation.file_id
            info_media = {"type": "gif", "file_id": file_id}
    elif len(message.text.split(" ")) == 2:
        info_media = {"type": "photo", "file_id": "https://i.imgur.com/jR5ABCc.png"}
    current_time = time.time()
    uptime_seconds = int(round(current_time - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    ping_start_time = time.time()
    await message.delete()
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000, 1)
    bot_name = "🤖Hack337 UserBot v2.0 Pro🤖\nTG: https://t.me/hack337userbot"
    caption = f"```info\n{bot_name}\nPing: {ping_time}ms\nUptime: {uptime}```"
    if info_media:
        if info_media["type"] == "photo":
            await app.send_photo(
                chat_id=message.chat.id,
                photo=info_media["file_id"],
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await app.send_animation(
                chat_id=message.chat.id,
                animation=info_media["file_id"],
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )

@app.on_message(filters.me & filters.command(["restart","рестарт","куыефке", "кые", "rst"], prefixes=prefix_userbot))
async def evaluate(client, message):
    msg = await message.edit('**🔄 Твой Hack337 UserBot перезагружается...**')
    restart_script(msg.id, msg.chat.id)

@app.on_message(filters.me & filters.command(["lm", "лм", "дь"], prefixes=prefix_userbot))
def load_module_msg(client, message):
    reply = message.reply_to_message
    if reply and reply.document:
        name = reply.document.file_name
        if name.endswith(".py"):
            if not os.path.exists("modules/" + name):
                message.edit(f"```lm\n Скачивание модуля... \n```")
                reply._client.download_media( reply.document.file_id , "modules/" + name)
                message.edit(f"```lm\n Поиск зависимостей... \n```")
                with open("modules/" + name, 'r') as file:
                    lines = []
                    for _ in range(3):
                        line = file.readline()
                        if not line:
                            break
                        lines.append(line.strip())
                errors = []
                for line in lines:
                    if line.startswith("# requires: "):
                        pips = line.replace("# requires: ", "").split(" ")
                        message.edit(f"```lm\n Установка зависимостей... \n```")
                        for package_name in pips:
                            try:
                                install_package(package_name)
                            except Exception as e:
                                errors.append(package_name)
                                message.edit(f"```lm\n Ошибка при установке {package_name}... \n```")
                if errors:
                    message.edit(f"```lm\n Ошибка при установке {', '.join(errors)} \n```")
                else:
                    message.edit(f"```lm\n Модуль успешно установлен. \n```")
            else:
                message.edit(f"```lm\n Такой модуль уже установлен. \n```")

@app.on_message(filters.me & filters.command(["ulm", "улм", "гдь"], prefixes=prefix_userbot))
def unload_module_msg(client, message):
    if len(message.text.split(" ")) == 2:
        mname = message.text.split(" ",1)[1]+".py"
        if os.path.exists("modules/" + mname):
            message.edit(f"```ulm\n Удаление модуля... \n```")
            try:
                os.remove("modules/" + mname)
            except Exception as e:
                message.edit(f"```ulm\n Ошибка при удалении {mname}... \n```")
            message.edit(f"```ulm\n Модуль успешно удалён. \n```")
        else:
            message.edit(f"```ulm\n Такой модуль не установлен. \n```")
    else:
        message.edit(f"```ulm\n Неверный синтаксис. \n```")

@app.on_message(filters.me & filters.command(["ping", "пинг", "зштп"], prefixes=prefix_userbot))
def ping(_, message):
    ping_start_time = time.time()
    msg = message.edit("🌕")
    ping_end_time = time.time()
    ping_time = round((ping_end_time - ping_start_time) * 1000)
    uptime_seconds = int(round(time.time() - start_time))
    uptime = str(timedelta(seconds=uptime_seconds))
    msg.edit(f"```ping\n 🕛Ваш пинг: {ping_time} мс\nUptime: {uptime} \n```")

@app.on_message(filters.me & filters.command(["гзв", "upd", "update"], prefixes=prefix_userbot))
def update(_, message):
    try:
        message.edit(f"```update\n Скачивание обновления... \n```")
        response = requests.get("https://raw.githubusercontent.com/y9hack337/uBot/main/bot.py")
        response.raise_for_status()
        message.edit(f"```update\n Запись обновления в файл... \n```")
        with open("bot.py", "wb") as f:
            f.write(response.content)
        message.edit(f"```update\n Обновление успешно установленно. \n Напиши .rst что бы применить изменения.```")
    except requests.exceptions.RequestException as e:
        message.edit(f"```update\n Ошибка при скачивании файла с GitHub... \n```")
    except OSError as e:
        message.edit(f"```update\n Ошибка при записи файла... \n```")
    except:
        message.edit(f"```update\n Ошибка... \n```")

async def getattrs(client, message):
    reply = message.reply_to_message
    return {
        "message": message,
        "reply": reply,
        "r": reply,
        "event": message,
        "chat": message.chat,
        "m": message,
        "c": client,
        "client": client,
        "app": client,
    }

@app.on_message(filters.me & filters.command(["eval","e"], prefixes=prefix_userbot))
async def evaluate(client, message):
    try:
        result = await meval(
            message.text.split(" ",1)[1],
            globals(),
            **await getattrs(client, message),
        )
    except Exception as e:
        await message.reply_text(f"Error {e}")
        return
    if callable(getattr(result, "stringify", None)):
        result = str(result.stringify())
    await message.reply_text(f'Request: \n{message.text.split(" ",1)[1]}\nResult:\n{str(result)}', parse_mode=ParseMode.DISABLED)

@app.on_message(filters.me & filters.command(["terminal", "t"], prefixes=prefix_userbot))
async def terminal_command(client, message):
    try:
        command = message.text.split(" ", 1)[1]
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes[str(message.id)] = process
        await message.edit_text(f"⌨️<b> Системная команда: </b><code>{command}</code>\n<b>Процесс ID: </b><code>{process.pid}</code>", parse_mode=ParseMode.HTML)
        stdout, stderr = await process.communicate()
        result = stdout.decode('utf-8').strip()
        error = stderr.decode('utf-8').strip()
        return_code = process.returncode
        output = f"📼<b> Вывод:</b>\n<code>{result if result else 'Нет вывода'}</code>"
        if error:
            output += f"\n🚫<b>Ошибка:</b>\n<code>{error}</code>"
        await message.edit_text(f"⌨️<b> Системная команда: </b><code>{command}</code>\n<b>Код выхода: </b><code>{return_code}</code>\n{output}", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.edit_text(f"<b>Ошибка: </b><code>{e}</code>", parse_mode=ParseMode.HTML)
    try:
        processes.pop(str(message.id))
    except:pass


@app.on_message(filters.me & filters.command(["terminate", "kill"], prefixes=prefix_userbot))
async def terminate_process(client, message):
    try:
        force_kill = "-f" in message.text
        reply = message.reply_to_message
        if not reply or str(reply.id) not in processes:
            await message.edit_text("Не найден процесс для завершения. Ответьте на сообщение с командой.", parse_mode=ParseMode.HTML)
            return
        process = processes.pop(str(reply.id))
        pid = process.pid
        if force_kill:
            os.kill(pid, signal.SIGKILL)
            await message.edit_text(f"Процесс с ID {pid} был принудительно завершен.", parse_mode=ParseMode.HTML)
        else:
            process.terminate()  # Обычное завершение процесса
            await message.edit_text(f"Процесс с ID {pid} был завершен.", parse_mode=ParseMode.HTML)
        
    except Exception as e:
        await message.edit_text(f"Ошибка: {e}", parse_mode=ParseMode.HTML)


def load_and_exec_modules():
    global message_id, chat_id, time_int, success, fail
    sys.path.append(os.path.abspath("modules"))

    for f in os.listdir("modules"):
        if f.endswith(".py"):
            module_name = f[:-3]
            print("--- Loading module "+module_name+"...")
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'register_commands'):
                    module.register_commands(app)
                    print("--- Module "+module_name+" loaded!")
                    success+=1
            except Exception as e:
                fail+=1
                print(f"Failed to load module {module_name}: {e}")
    print("--- All modules are loaded! ---")

    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "--message_id":
            message_id = int(sys.argv[i + 1])
        elif sys.argv[i] == "--chat_id":
            chat_id = int(sys.argv[i + 1])
        elif sys.argv[i] == "--time":
            time_int = int(sys.argv[i + 1])

async def edit_restart_message():
    global message_id, chat_id, time_int, success, fail
    if message_id is not None and chat_id is not None and time_int is not None:
        await app.edit_message_text(int(chat_id), int(message_id), f"**⏱ Перезагрузка успешна! {random.choice(cats)}\nПерезагрузка заняла {int(time.time() - time_int)} сек\nУспешно загружено {success} модулей и {fail} с ошибкой.**")

load_and_exec_modules()

async def main():
    await app.start()
    await edit_restart_message()
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
