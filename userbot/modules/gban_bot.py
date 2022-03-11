"""Globally Ban users from all the
Group Administrations bots where you are SUDO
Available Commands:
.gban REASON
.ungban REASON"""
import asyncio
from userbot.utils import toni_cmd
from userbot import (
    G_BAN_LOGGER_GROUP,
    CMD_HANDLER as cmd,
    ALIVE_NAME,
    CMD_HELP,
    bot,
)


@toni_cmd(pattern="gbanb(?: |$)(.*)")
async def _(event):
    if G_BAN_LOGGER_GROUP is None:
        await event.edit("Set G_BAN_LOGGER_GROUP in vars otherwise module won't work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        if r.forward:
            r_from_id = r.forward.from_id or r.from_id
        else:
            r_from_id = r.from_id
        await bot.send_message(
            G_BAN_LOGGER_GROUP,
            "/gban [user](tg://user?id={}) {}".format(r_from_id, reason)
        )
    await event.delete()
    await event.reply("**gbanning...**")
    asyncio.sleep(3.5)
    await event.edit(f"**User gbanned by {ALIVE_NAME}**")
    asyncio.sleep(5)
    await event.delete()


@toni_cmd(pattern="ungbanb(?: |$)(.*)")
async def _(event):
    if G_BAN_LOGGER_GROUP is None:
        await event.edit("Set G_BAN_LOGGER_GROUP in vars otherwise module won't work.")
        return
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        r_from_id = r.from_id
        await bot.send_message(
            G_BAN_LOGGER_GROUP,
            "/ungban [user](tg://user?id={}) {}".format(r_from_id, reason)
        )
    await event.delete()
    await event.reply("**ungbanning...**")
    asyncio.sleep(3.5)
    await event.edit(f"**User ungbanned by {ALIVE_NAME}**")
    asyncio.sleep(5)
    await event.delete()

CMD_HELP.update({
    "gbanbot": f"`{cmd}gbanb`\
    \nUsage: globally Ban Bot.\
    \n\n`{cmd}ungbanb` :\
    \nUsage: Cancel globally Ban Bot."
})
