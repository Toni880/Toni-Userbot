# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

import asyncio
from platform import uname

from userbot import (
    CMD_HANDLER as cmd,
    ICON_HELP,
    CMD_HELP,
    CHANNEL,
)
from userbot.utils import (
    toni_cmd,
    edit_or_reply,
    edit_delete,
)

modules = CMD_HELP

@toni_cmd(pattern="help(?: |$)(.*)")
async def help(event):
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await edit_or_reply(event, str(CMD_HELP[args]))
        else:
            await edit_delete(event, f"`{args}` **Bukan Nama Modul yang Valid.**")
    else:
        user = await event.client.get_me()
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += f"`\t\t\t{ICON_HELP}\t\t\t"
        await edit_or_reply(
            event,
            f"**✦ Daftar Perintah Untuk [Tonic-Userbot](https://github.com/Tonic990/Tonic-Userbot):**\n"
            f"**✦ Jumlah** `{len(modules)}` **Modules**\n"
            f"**✦ Owner:** [{user.first_name}](tg://user?id={user.id})\n\n"
            f"{ICON_HELP}   {string}"
            f"\n\nSupport @{CHANNEL}",
        )
        await event.reply(
            f"\n**Contoh Ketik** `{cmd}help afk` **Untuk Melihat Informasi Module**"
        )
