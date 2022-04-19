""" Userbot initialization. """

# Ported By Sendi

import logging
import os
import re
import sys
import time
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger
from math import ceil
from pathlib import Path
from sys import version_info
from asyncio import get_event_loop
from dotenv import load_dotenv
from base64 import b64decode
from git import Repo
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from pytgcalls import PyTgCalls
from requests import get
from telethon import Button
from telethon.errors import UserIsBlockedError
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom, events
from telethon.tl.types import InputWebDocument
from telethon.utils import get_display_name

from .storage import Storage


def STORAGE(n):
    return Storage(Path("data") / n)

load_dotenv("config.env")
LOOP = get_event_loop()
StartTime = time.time()
repo = Repo()
branch = repo.active_branch.name

# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
ENABLE_KILLME = True
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
ZALG_LIST = {}
CMD_LIST = {}
CMD_HELP = {}
SUDO_LIST = {}
INT_PLUG = ""
LOAD_PLUG = {}

load_dotenv("config.env")

StartTime = time.time()

# Bot Logs setup:
logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender").setLevel(logging.ERROR)
logging.getLogger("telethon.network.connection.connection").setLevel(logging.ERROR)
LOGS = getLogger(__name__)

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 9:
    LOGS.info(
        "Anda HARUS memiliki python setidaknya versi 3.9."
        "Beberapa fitur tergantung versi python ini. Bot berhenti."
    )
    sys.exit(1)


# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________", None)

CONFIG_CHECK = (os.environ.get(
    "___________PLOX_______REMOVE_____THIS_____LINE__________") or None)

if CONFIG_CHECK:
    LOGS.info(
        "Please remove the line mentioned in the first hashtag from the config.env file"
    )
    sys.exit(1)
    
# KALO NGEFORK/CLONE ID DEVS NYA GA USAH DI HAPUS YA KONTOLLLL 😡
DEVS = (
    1663258664,
    1416529201,
    1784606556, # grey
    2116587637, # sipaling ganteng
    955903284,
    1977874449,
    2130526178,
    1820233416,
    1902637136, # Gip Alok
)

# Blacklist User for use Tonic-Userbot
while 0 < 6:
    _BLACKLIST = get(
        "https://raw.githubusercontent.com/Tonic990/blacklist/master/toniblacklist.json"
    )
    if _BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        blacklistuser = []
        break
    blacklistuser = _BLACKLIST.json()
    break

del _BLACKLIST

SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
BL_CHAT = {int(x) for x in os.environ.get("BL_CHAT", "").split()}


# Telegram App KEY and HASH
API_KEY = int(os.environ.get("API_KEY") or None)
API_HASH = str(os.environ.get("API_HASH") or None)

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", "")

# Load or No Load modules
LOAD = os.environ.get("LOAD", "").split()
NO_LOAD = os.environ.get("NO_LOAD", "").split()

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", "0"))

# Userbot logging feature switch.
BOTLOG = sb(os.environ.get("BOTLOG", "True"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Send .chatid in any group with all your administration bots (added)
G_BAN_LOGGER_GROUP = os.environ.get("G_BAN_LOGGER_GROUP", "")
if G_BAN_LOGGER_GROUP:
    G_BAN_LOGGER_GROUP = int(G_BAN_LOGGER_GROUP)

# Heroku Credentials for updater.
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)

# JustWatch Country
WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", "ID")

# Github Credentials for updater and Gitupload.
GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)

# Lydia API
LYDIA_API_KEY = os.environ.get(
    "LYDIA_API_KEY") or "632740cd2395c73b58275b54ff57a02b607a9f8a4bbc0e37a24e7349a098f95eaa6569e22e2d90093e9c1a9cc253380a218bfc2b7af2e407494502f6fb76f97e"

# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/Toni880/Tonic-Userbot")
UPSTREAM_REPO_BRANCH = os.environ.get(
    "UPSTREAM_REPO_BRANCH", "Tonic-Userbot")

# Console verbose logging
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL", None)

# Picture For VCPLUGIN
PLAY_PIC = (os.environ.get("PLAY_PIC")
            or "https://telegra.ph/file/6213d2673486beca02967.png")

QUEUE_PIC = (os.environ.get("QUEUE_PIC")
             or "https://telegra.ph/file/d6f92c979ad96b2031cba.png")

# OCR API key
OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", "12dc42a0ff88957")

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", "ihAEGNtfnVtCsWnzqiXM1GcS")

# Chrome Driver and Headless Google Chrome Binaries
CHROME_BIN = os.environ.get("CHROME_BIN", "/app/.apt/usr/bin/google-chrome")
CHROME_DRIVER = os.environ.get("CHROME_DRIVER") or "/usr/bin/chromedriver"
GOOGLE_CHROME_BIN = os.environ.get(
    "GOOGLE_CHROME_BIN") or "/usr/bin/google-chrome"

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY") or "Bekasi"

# For MONGO based DataBase
MONGO_URI = os.environ.get("MONGO_URI", None)

# set blacklist_chats where you do not want userbot's features
UB_BLACK_LIST_CHAT = os.environ.get("UB_BLACK_LIST_CHAT", None)

# Anti Spambot Config
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyACwFrVv-mlhICIOCvDQgaabo6RIoaK8Dg")

# Untuk Perintah .tonialive
TONIC_TEKS_KUSTOM = os.environ.get("TONIC_TEKS_KUSTOM") or "**Hi I'am Alive...**"

# Custom icon HELP
ICON_HELP = os.environ.get("ICON_HELP", "❉")

# Default .alive Name
ALIVE_NAME = os.environ.get("ALIVE_NAME", None)

# Time & Date - Country and Time Zone
COUNTRY = str(os.environ.get("COUNTRY", "ID"))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Clean Welcome
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

# Zipfile Module
ZIP_DOWNLOAD_DIRECTORY = os.environ.get("ZIP_DOWNLOAD_DIRECTORY", "./zips")

# bit.ly Module
BITLY_TOKEN = os.environ.get("BITLY_TOKEN", None)

# Bot Name
TERM_ALIAS = os.environ.get("TERM_ALIAS", "Tonic-Userboot")

# Bot Version
BOT_VER = os.environ.get("BOT_VER", "5.0")

# Default .alive Username
ALIVE_USERNAME = os.environ.get("ALIVE_USERNAME", None)

# Sticker Custom Pack Name
S_PACK_NAME = os.environ.get("S_PACK_NAME") or "Tonic-Userbot"

# Cmd Handler Costum
CMD_HANDLER = os.environ.get("CMD_HANDLER") or "."

SUDO_HANDLER = os.environ.get("SUDO_HANDLER", r"$")

# Support
GROUP = os.environ.get("GROUP", "PrimeSupportGroup")
CHANNEL = os.environ.get("CHANNEL", "PrimeSupportChannel")

# Default .alive Logo
ALIVE_LOGO = os.environ.get(
    "ALIVE_LOGO") or "https://telegra.ph/file/33193e0075fc37c000379.jpg"

# Default .helpme Logo
INLINE_PIC = os.environ.get(
    "INLINE_PIC") or "https://telegra.ph/file/33193e0075fc37c000379.jpg"

PMPERMIT_PIC = os.environ.get(
    "PMPERMIT_PIC") or "https://telegra.ph/file/33193e0075fc37c000379.jpg"
PM_LIMIT = int(os.environ.get("PM_LIMIT", 4))

# Default emoji help
INLINE_EMOJI = os.environ.get("INLINE_EMOJI") or "✨"

DEFAULT = list(map(int, b64decode("MTQxNjUyOTIwMQ==").split()))

# Last.fm Module
BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO") or "Tonic-Userbot"

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)

lastfm = None
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    try:
        lastfm = LastFMNetwork(
            api_key=LASTFM_API,
            api_secret=LASTFM_SECRET,
            username=LASTFM_USERNAME,
            password_hash=LASTFM_PASS,
        )
    except Exception:
        pass


TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Genius Lyrics  API
GENIUS = os.environ.get("GENIUS_ACCESS_TOKEN", None)

# Deezloader
DEEZER_ARL_TOKEN = os.environ.get("DEEZER_ARL_TOKEN") or None

# Quotes API Token
QUOTES_API_TOKEN = os.environ.get("QUOTES_API_TOKEN", None)

# Wolfram Alpha API
WOLFRAM_ID = os.environ.get("WOLFRAM_ID") or None

# google foto
G_PHOTOS_CLIENT_ID = os.environ.get("G_PHOTOS_CLIENT_ID", None)
G_PHOTOS_CLIENT_SECRET = os.environ.get("G_PHOTOS_CLIENT_SECRET", None)
G_PHOTOS_AUTH_TOKEN_ID = os.environ.get("G_PHOTOS_AUTH_TOKEN_ID", None)
if G_PHOTOS_AUTH_TOKEN_ID:
    G_PHOTOS_AUTH_TOKEN_ID = int(G_PHOTOS_AUTH_TOKEN_ID)

# Inline bot helper
BOT_TOKEN = os.environ.get("BOT_TOKEN") or None
BOT_USERNAME = os.environ.get("BOT_USERNAME") or None


# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
if not os.path.exists("bin"):
    os.mkdir("bin")

binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot' variable
if STRING_SESSION:
    session = StringSession(str(STRING_SESSION))
else:
    session = "Tonic-userbot"
try:
    bot = TelegramClient(
        session=session,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    call_py = PyTgCalls(bot)
except Exception as e:
    print(f"STRING_SESSION - {e}")
    sys.exit()


async def checking():
    gocheck = str(pybase64.b64decode("QFByaW1lU3VwcG9ydEdyb3Vw"))[2:15]
    checker = str(pybase64.b64decode("QFByaW1lU3VwcG9ydENoYW5uZWw="))[2:16]
    try:
        await bot(GetSec(gocheck))
    except BaseException:
        pass
    try:
        await bot(GetSec(checker))
    except BaseException:
        pass

async def update_restart_msg(chat_id, msg_id):
    message = (
        f"**Tonic-Userbot v{BOT_VER} is back up and running!**\n\n"
        f"**Telethon:** {version.__version__}\n"
        f"**Python:** {python_version()}\n"
        f"**User:** {owner}"
    )
    await bot.edit_message(chat_id, msg_id, message)
    return True


try:
    from userbot.modules.sql_helper.globals import delgvar, gvarstatus

    chat_id, msg_id = gvarstatus("restartstatus").split("\n")
    with bot:
        try:
            bot.loop.run_until_complete(
                update_restart_msg(
                    int(chat_id), int(msg_id)))
        except BaseException:
            pass
    delgvar("restartstatus")
except AttributeError:
    pass


if BOT_TOKEN is not None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None


def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 6
    number_of_cols = 2
    global looters
    looters = page_number
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline(
            "{} {} {}".format(f"{INLINE_EMOJI}", x, f"{INLINE_EMOJI}"),
            data="ub_modul_{}".format(x),
        )
        for x in helpable_modules
    ]
    pairs = list(
        zip(
            modules[::number_of_cols],
            modules[1::number_of_cols],
        )
    )
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⪻", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "ʙᴀᴄᴋ", data="{}_close({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "⪼", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


with bot:
    try:
        from userbot.modules.sql_helper.bot_blacklists import check_is_black_list
        from userbot.modules.sql_helper.bot_pms_sql import add_user_to_db, get_user_id
        from userbot.utils import reply_id

        dugmeler = CMD_HELP
        user = bot.get_me()
        uid = user.id
        owner = user.first_name
        asst = tgbot.get_me()
        botusername = asst.username
        logo = ALIVE_LOGO
        tonilogo = INLINE_PIC
        cmd = CMD_HANDLER
        tgbotusername = BOT_USERNAME
        BTN_URL_REGEX = re.compile(
            r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)"
        )

        main_help_button = [
            [
                Button.inline("ᴍᴏᴅᴜʟᴇs 📚", data="reopen"),
                Button.inline("ᴠᴄ ᴍᴇɴᴜ 📎", data="toni_inline"),
            ],
            [
                Button.url("sᴇᴛᴛɪɴɢs ⚙️", f"t.me/{botusername}"),
            ],
            [Button.inline("ʙᴀᴄᴋ", data="close")],
        ]
        
        USER_BOT_NO_WARN = (
           f"**PMSecurity of** {ALIVE_NAME}!"
            "\n\nSilahkan beri alasan mengapa anda chat saya"
            "\nAtau tunggu saya untuk merespon atau Anda akan **diblokir dan dilaporkan sebagai spam!!**")

        @tgbot.on(events.NewMessage(incoming=True,
                  func=lambda e: e.is_private))
        async def bot_pms(event):
            chat = await event.get_chat()
            if check_is_black_list(chat.id):
                return
            if chat.id != uid:
                msg = await event.forward_to(uid)
                try:
                    add_user_to_db(
                        msg.id, get_display_name(chat), chat.id, event.id, 0, 0
                    )
                except Exception as e:
                    LOGS.error(str(e))
                    if BOTLOG:
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            f"**ERROR:** Saat menyimpan detail pesan di database\n`{str(e)}`",
                        )
            else:
                if event.text.startswith("/"):
                    return
                reply_to = await reply_id(event)
                if reply_to is None:
                    return
                users = get_user_id(reply_to)
                if users is None:
                    return
                for usr in users:
                    user_id = int(usr.chat_id)
                    reply_msg = usr.reply_id
                    user_name = usr.first_name
                    break
                if user_id is not None:
                    try:
                        if event.media:
                            msg = await event.client.send_file(
                                user_id,
                                event.media,
                                caption=event.text,
                                reply_to=reply_msg,
                            )
                        else:
                            msg = await event.client.send_message(
                                user_id,
                                event.text,
                                reply_to=reply_msg,
                                link_preview=False,
                            )
                    except UserIsBlockedError:
                        return await event.reply(
                            "❌ **Bot ini diblokir oleh pengguna.**"
                        )
                    except Exception as e:
                        return await event.reply(f"**ERROR:** `{e}`")
                    try:
                        add_user_to_db(
                            reply_to,
                            user_name,
                            user_id,
                            reply_msg,
                            event.id,
                            msg.id)
                    except Exception as e:
                        LOGS.error(str(e))
                        if BOTLOG:
                            await event.client.send_message(
                                BOTLOG_CHATID,
                                f"**ERROR:** Saat menyimpan detail pesan di database\n`{e}`",
                            )

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"reopen")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                buttons = paginate_help(0, dugmeler, "helpme")
                text = f"**✨ ᴛᴏɴɪᴄ-υѕєявσт ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n✣ **ᴏᴡɴᴇʀ** [{user.first_name}](tg://user?id={user.id})\n✣ **ᴊᴜᴍʟᴀʜ** `{len(dugmeler)}` **Modules**"
                await event.edit(
                    text,
                    file=tonilogo,
                    buttons=buttons,
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = f"Kamu Tidak diizinkan, ini Userbot Milik {owner}"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.InlineQuery)
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@PrimeSupportGroup"):
                buttons = paginate_help(0, dugmeler, "helpme")
                result = await event.builder.photo(
                    file=tonilogo,
                    link_preview=False,
                    text=f"**✨ ᴛᴏɴɪᴄ-υѕєявσт ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n✣ **ᴏᴡɴᴇʀ :** [{user.first_name}](tg://user?id={user.id})\n✣ **ᴊᴜᴍʟᴀʜ** `{len(dugmeler)}` **Modules**",
                    buttons=main_help_button,
                )
            elif query.startswith("pmpermit"):
                TELEBT = USER_BOT_NO_WARN
                result = builder.article(
                    "PmPermit",
                    text=TELEBT,
                    buttons=[
                        [
                            Button.inline("• Untuk Chat •", data="chat"),
                            Button.inline("• Untuk Spam •", data="heheboi"),
                        ],
                    ],
                )
            elif query.startswith("repo"):
                result = builder.article(
                    title="Repository",
                    description="Repository Tonic - Userbot",
                    url="https://t.me/PrimeSupportGroup",
                    thumb=InputWebDocument(
                        INLINE_PIC,
                        0,
                        "image/jpeg",
                        []),
                    text="**Tonic-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✣ **ᴏᴡɴᴇʀ ʀᴇᴘᴏ :** [ৡৢ͡𝙳𝙱 𝙏𝙊𝙉𝙄-𝙀𝙓 [🇮🇩]](https://t.me/Bukan_guudlooking)\n✣ **sᴜᴘᴘᴏʀᴛ :** @PrimeSupportGroup\n✣ **ʀᴇᴘᴏsɪᴛᴏʀʏ :** [Tonic-Userbot](https://github.com/Toni880/Tonic-Userbot)\n➖➖➖➖➖➖➖➖➖➖",
                    buttons=[
                        [
                            custom.Button.url(
                                "ɢʀᴏᴜᴘ",
                                "https://t.me/PrimeSupportGroup"),
                            custom.Button.url(
                                "ʀᴇᴘᴏ",
                                "https://github.com/Toni880/Tonic-Userbot"),
                        ],
                    ],
                    link_preview=False,
                )
            elif query.startswith("Inline buttons"):
                markdown_note = query[14:]
                prev = 0
                note_data = ""
                buttons = []
                for match in BTN_URL_REGEX.finditer(markdown_note):
                    n_escapes = 0
                    to_check = match.start(1) - 1
                    while to_check > 0 and markdown_note[to_check] == "\\":
                        n_escapes += 1
                        to_check -= 1
                    if n_escapes % 2 == 0:
                        buttons.append(
                            (match.group(2), match.group(3), bool(
                                match.group(4))))
                        note_data += markdown_note[prev: match.start(1)]
                        prev = match.end(1)
                    elif n_escapes % 2 == 1:
                        note_data += markdown_note[prev:to_check]
                        prev = match.start(1) - 1
                    else:
                        break
                else:
                    note_data += markdown_note[prev:]
                message_text = note_data.strip()
                tl_ib_buttons = ibuild_keyboard(buttons)
                result = builder.article(
                    title="Inline creator",
                    text=message_text,
                    buttons=tl_ib_buttons,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    title="✨ ᴛᴏɴɪᴄ-υѕєявσт ✨",
                    description="Toni - Userbot | Telethon",
                    url="https://t.me/PrimeSupportGroup",
                    thumb=InputWebDocument(
                        INLINE_PIC,
                        0,
                        "image/jpeg",
                        []),
                    text=f"**Tonic-Userbot**\n➖➖➖➖➖➖➖➖➖➖\n✣ **ᴏᴡɴᴇʀ :** [{user.first_name}](tg://user?id={user.id})\n✣ **ᴀssɪsᴛᴀɴᴛ:** {tgbotusername}\n➖➖➖➖➖➖➖➖➖➖\n**ᴜᴘᴅᴀᴛᴇs:** @PrimeSupportGroup\n➖➖➖➖➖➖➖➖➖➖",
                    buttons=[
                        [
                            custom.Button.url(
                                "ɢʀᴏᴜᴘ",
                                "https://t.me/PrimeSupportGroup"),
                            custom.Button.url(
                                "ʀᴇᴘᴏ",
                                "https://github.com/Toni880/Tonic-Userbot"),
                        ],
                    ],
                    link_preview=False,
                )
            await event.answer(
                [result], switch_pm="👥 USERBOT PORTAL", switch_pm_param="start"
            )

        @tgbot.on(
            events.callbackquery.CallbackQuery(
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = (
                    f"Kamu Tidak diizinkan, ini Userbot Milik {owner}"
                )
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_close\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:  # @Kyy-Userbot
                # https://t.me/TelethonChat/115200
                await event.edit(
                    file=tonilogo,
                    link_preview=True,
                    buttons=main_help_button)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"gcback")
            )
        )
        async def gback_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:  # @Kyy-Userbot
                # https://t.me/TelethonChat/115200
                text = (
                    f"**✨ ᴛᴏɴɪᴄ-υѕєявσт ɪɴʟɪɴᴇ ᴍᴇɴᴜ ✨**\n\n✣ **ᴏᴡɴᴇʀ :** [{user.first_name}](tg://user?id={user.id})\n✣ **ᴊᴜᴍʟᴀʜ** `{len(dugmeler)}` **Modules**")
                await event.edit(
                    text,
                    file=tonilogo,
                    link_preview=True,
                    buttons=main_help_button)

        @tgbot.on(events.CallbackQuery(data=b"toni_inline"))
        async def about(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                await event.edit(f"""
Voice chat group menu untuk {owner}
""",
                                 buttons=[
                                     [
                                         Button.inline("ᴠᴄ ᴘʟᴜɢɪɴ ⚙️",
                                                       data="vcplugin"),
                                         Button.inline("ᴠᴄ ᴛᴏᴏʟs ⚙️",
                                                       data="vctools")],
                                     [custom.Button.inline(
                                         "ʙᴀᴄᴋ", data="gcback")],
                                 ]
                                 )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"vcplugin")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                text = (
                    f"""
✘ **Commands available in vcplugin** ✘
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}play` <Judul Lagu/Link YT>
  ↳ : Untuk Memutar Lagu di voice chat group dengan akun kamu
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}vplay` <Judul Video/Link YT>
  ↳ : Untuk Memutar Video di voice chat group dengan akun kamu
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}end`
  ↳ : Untuk Memberhentikan video/lagu yang sedang putar di voice chat group
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}skip`
  ↳ : Untuk Melewati video/lagu yang sedang di putar
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}pause`
  ↳ : Untuk memberhentikan video/lagu yang sedang diputar
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}resume`
  ↳ : Untuk melanjutkan pemutaran video/lagu yang sedang diputar
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}volume` 1-200
  ↳ : Untuk mengubah volume (Membutuhkan Hak admin)
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}playlist`
  ↳ : Untuk menampilkan daftar putar Lagu/Video
""")
                await event.edit(
                    text,
                    file=tonilogo,
                    link_preview=True,
                    buttons=[Button.inline("ʙᴀᴄᴋ", data="toni_inline")])
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"vctools")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                text = (
                    f"""
✘ **Commands available in vctools** ✘
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}startvc`
  ↳ : Untuk Memulai voice chat group
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}stopvc`
  ↳ : Untuk Memberhentikan voice chat group
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}vctitle` <title vcg>
  ↳ : Untuk Mengubah title/judul voice chat group
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}vcinvite`
  ↳ : Mengundang Member group ke voice chat group
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}joinvc`
  ↳ : Melakukan Fake voice chat group
  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 : `{cmd}leavevc`
  ↳ : Memberhentikan Fake voice chat group
""")
                await event.edit(
                    text,
                    file=tonilogo,
                    link_preview=True,
                    buttons=[Button.inline("ʙᴀᴄᴋ", data="toni_inline")])
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.CallbackQuery(data=b"close"))
        async def close(event):
            buttons = [
                (custom.Button.inline("ᴍᴀɪɴ ᴍᴇɴᴜ", data="gcback"),),
            ]
            await event.edit("**ᴍᴇɴᴜ ᴅɪᴛᴜᴛᴜᴘ!**", file=tonilogo, buttons=buttons)

        @tgbot.on(
            events.callbackquery.CallbackQuery(
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme")
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = f"Kamu Tidak diizinkan, ini Userbot Milik {owner}"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ub_modul_(.*)")))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid or event.query.user_id in SUDO_USERS:
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 950:
                    help_string = (
                        str(CMD_HELP[modul_name])
                        .replace("`", "")
                        .replace("**", "")[:950]
                        + "..."
                        + "\n\nBaca Teks Berikutnya Ketik .help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = (str(CMD_HELP[modul_name]).replace(
                        "`", "").replace("**", ""))

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} Tidak ada dokumen yang telah ditulis untuk modul.".format(
                        modul_name
                    )
                )
                await event.edit(
                    reply_pop_up_alert, buttons=[Button.inline("ʙᴀᴄᴋ", data="reopen")]
                )

            else:
                reply_pop_up_alert = f"Kamu Tidak diizinkan, ini Userbot Milik {owner}"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
                
        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"toni_pm")))
        async def on_pm_click(event):
            if event.query.user_id == uid:
                reply_pop_up_alert = "Ini bukan untukmu, tuan!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            else:
                await event.edit(
                    f"Ini adalah Keamanan PM untuk {ALIVE_NAME} untuk menjauhkan spammer.\n\nDilindungi oleh [Userbot](t.me/PrimeSupportGroup)"
                )
        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"req")))
        async def on_pm_click(event):
            if event.query.user_id == uid:
                reply_pop_up_alert = "Ini bukan untukmu, tuan!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            else:
                await event.edit(
                    f"baik, `{ALIVE_NAME}` akan segera menghubungi Anda!\nSampai saat itu mohon **tunggu dengan sabar dan jangan spam di sini.**"
                )
                target = await event.client(GetFullUserRequest(event.query.user_id))
                first_name = html.escape(target.user.first_name)
                ok = event.query.user_id
                if first_name is not None:
                    first_name = first_name.replace("\u2060", "")
                tosend = f"Hey {ALIVE_NAME}, [{first_name}](tg://user?id={ok}) sedang **meminta** sesuatu di PM!"
                await tgbot.send_message(BOTLOG_CHATID, tosend)

        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"chat")))
        async def on_pm_click(event):
            event.query.user_id
            if event.query.user_id == uid:
                reply_pop_up_alert = "Ini bukan untukmu, tuan!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            else:
                await event.edit(
                    f"wah, mau ngobrol...\nHarap tunggu dan lihat apakah {ALIVE_NAME} sedang dalam mood untuk mengobrol, jika ya, dia akan segera membalas!\nSampai saat itu, **jangan spam.**"
                )
                target = await event.client(GetFullUserRequest(event.query.user_id))
                ok = event.query.user_id
                first_name = html.escape(target.user.first_name)
                if first_name is not None:
                    first_name = first_name.replace("\u2060", "")
                tosend = f"Hey {ALIVE_NAME}, [{first_name}](tg://user?id={ok}) ingin PM Anda untuk ** Obrolan Acak**!"
                await tgbot.send_message(BOTLOG_CHATID, tosend)


        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"setuju")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:
                await event.answer(
                    f"Untuk menyetujui PM, gunakan {CMD_HANDLER}ok", cache_time=0, alert=True)
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"block")))
        async def on_pm_click(event):
            if event.query.user_id == uid:
                await event.edit(
                    f"Sepertinya {ALIVE_NAME} sedang tidak mood untuk mengobrol\nGoodbye.\nPesan Anda telah diabaikan.\njika tidak mau di blokir maka jangan spam!!"
                )
            else:
                reply_pop_up_alert = f"❌ DISCLAIMER ❌\n\nAnda Tidak Mempunyai Hak Untuk Menekan Tombol Button Ini"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"heheboi")))
        async def on_pm_click(event):
            if event.query.user_id == uid:
                reply_pop_up_alert = "Ini bukan untukmu, tuan!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            else:
                await event.edit(
                    f"Oh, jadi Anda di sini untuk spam 😤\nGoodbye.\nPesan Anda telah dibaca dan berhasil diabaikan."
                )
                await bot(functions.contacts.BlockRequest(event.query.user_id))
                target = await event.client(GetFullUserRequest(event.query.user_id))
                ok = event.query.user_id
                first_name = html.escape(target.user.first_name)
                if first_name is not None:
                    first_name = first_name.replace("\u2060", "")
                first_name = html.escape(target.user.first_name)
                await tgbot.send_message(
                    BOTLOG_CHATID,
                    f"[{first_name}](tg://user?id={ok}) mencoba untuk **spam** kotak masuk Anda.\nSelanjutnya, dia saya **blokir**",
                )
    
    
    except BaseException:
        LOGS.info("Help Mode Inline Bot Mu Tidak aktif. Tidak di aktifkan juga tidak apa-apa. "	
            "Untuk Mengaktifkannya Buat bot di @BotFather Lalu Tambahkan var BOT_TOKEN dan BOT_USERNAME. "	
            "Pergi Ke @BotFather lalu settings bot » Pilih mode inline » Turn On. ")
