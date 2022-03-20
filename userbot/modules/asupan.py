# 🍀 © @tofik_dn
# ⚠️ Do not remove credits


from userbot import CMD_HANDLER as cmd, CMD_HELP
from userbot.utils import toni_cmd
import random
from userbot import owner
from telethon.tl.types import InputMessagesFilterVideo


@toni_cmd(pattern="asupan$")
async def _(event):
    try:
        asupannya = [
            asupan
            async for asupan in event.client.iter_messages(
                "@Database_TonicUbot", filter=InputMessagesFilterVideo
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(asupannya),
            caption=f"ᴀsᴜᴘᴀɴ ʙʏ [{owner}](tg://user?id={aing.id})",
        )
        await event.delete()
    except Exception:
        await event.edit("Tidak bisa menemukan video asupan.")
        
@toni_cmd(pattern="phub$")
async def _(event):
    try:
        phub = [
            porn
            async for porn in event.client.iter_messages(
                "@TonicPorn", filter=InputMessagesFilterVideo
            )
        ]
        xx = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(phub),
            caption=f"ᴀsᴜᴘᴀɴ ʙʏ [{owner}](tg://user?id={xx.id})",
        )
        await event.delete()
    except Exception:
        await event.edit("Tidak bisa menemukan video asupan.")



CMD_HELP.update(
    {
        "asupan": f"**Plugin : **`asupan`\
        \n\n  •  **Syntax :** `{cmd}asupan`\
        \n  •  **Function : **Untuk Mengirim video asupan secara random.\
        \n\n  •  **Syntax :** `{cmd}phub`\
        \n  •  **Function : **Untuk Mengirim video phub secara random.\
    "
    }
)
