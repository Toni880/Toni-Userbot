# Credit @mrismanaziz

import sys
from telethon.utils import get_peer_id
from userbot import (
  BOT_TOKEN,
  BOT_VER as version,
  DEVS,
  LOGS,
  LOOP,
  STRING_SESSION,
  blacklistuser,
  call_py,
  tgbot,
  bot,
)
from userbot.modules.gcast import GCAST_BLACKLIST as GBL

EOL = "EOL\nTonic-UserBot v{}, Copyright © 2021-2022 ᴛᴏɴɪ• <https://github.com/Tonic990>"
MSG_BLACKLIST = "MAKANYA GA USAH BERTINGKAH GOBLOK, USERBOT {} GUA MATIIN NAJIS BANGET DIPAKE JAMET KEK LU.\nTonic-UserBot v{}, Copyright © 2021-2022 ᴛᴏɴɪ• <https://github.com/Tonic990>"

async def toni_client(client):
    client.me = await client.get_me()
    client.uid = get_peer_id(client.me)

def multi_toni():
    if 1416529201 not in DEVS:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if -1001578091827 not in GBL:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    if 1416529201 not in DEFAULT:
        LOGS.warning(EOL.format(version))
        sys.exit(1)
    failed = 0
    if STRING_SESSION:
        try:
            bot.start()
            call_py.start()
            LOOP.run_until_complete(toni_client(bot))
            user = bot.get_me()
            name = user.first_name
            uid = user.id
            LOGS.info(
                f"STRING_SESSION detected!\n┌ First Name: {name}\n└ User ID: {uid}\n——"
            )
            if user.id in blacklistman:
                LOGS.warning(MSG_BLACKLIST.format(name, version))
                sys.exit(1)
        except Exception as e:
            LOGS.info(str(e))
            
    if BOT_TOKEN:
        try:
            user = tgbot.get_me()
            name = user.first_name
            uname = user.username
            LOGS.info(
                f"BOT_TOKEN detected!\n┌ First Name: {name}\n└ Username: @{uname}\n——"
            )
        except Exception as e:
            LOGS.info(str(e))
            
    if not STRING_SESSION:
        failed += 1
    return failed
