""" Userbot start point """

import sys
from importlib import import_module

import requests
from pytgcalls import __version__ as pytgcalls
from pytgcalls import idle
from telethon import version

from userbot import (
    BOT_TOKEN,
    BOT_USERNAME,
    BOT_VER,
    BOTLOG_CHATID,
    DEVS, 
    LOGS,
    LOOP,
)
from userbot.clients import multi_toni, toni_userbot_on
from userbot.modules import ALL_MODULES
from userbot.utils import autobot, autopilot

try:
    for module_name in ALL_MODULES:
        imported_module = import_module(f"userbot.modules.{module_name}")
    client = multi_toni()
    total = 5 - client
    git()
    LOGS.info(f"Total Clients = {total} User")
    LOGS.info(f"Python Version - {python_version()}")
    LOGS.info(f"Telethon Version - {version.__version__}")
    LOGS.info(f"PyTgCalls Version - {pytgcalls.__version__}")
    LOGS.info(f"Tonic-Userbot Version - {BOT_VER} [🔥 BERHASIL DIAKTIFKAN! 🔥]")
except (ConnectionError, KeyboardInterrupt, NotImplementedError, SystemExit):
    pass
except BaseException as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)


LOOP.run_until_complete(toni_userbot_on())
if not BOTLOG_CHATID:
    LOOP.run_until_complete(autopilot())
if not BOT_TOKEN:
    LOOP.run_until_complete(autobot())
idle()
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass
