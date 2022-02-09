from telethon import Button

from userbot import BOTLOG, BOTLOG_CHATID, LOGS, tgbot




async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            await tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/33193e0075fc37c000379.jpg",
                caption="🌹 **Tonic UserBot Has Been Actived**!!\n━━━━━━━━━━━━━━━\n➠ **Userbot Version** - 5.0@master\n━━━━━━━━━━━━━━━\n➠ **Powered By:** @PrimeSupportChannel ",
                buttons=[(Button.url("ꜱᴜᴘᴘᴏʀᴛ", "https://t.me/PrimeSupportGroup"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
