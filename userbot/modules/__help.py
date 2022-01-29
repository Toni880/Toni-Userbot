import logging

from telethon.errors.rpcerrorlist import BotInlineDisabledError as noinline
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest

from userbot import BOT_USERNAME
from userbot import CMD_HANDLER as cmd
from userbot import bot
from userbot.events import toni_cmd

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


@bot.on(toni_cmd(outgoing=True, pattern=r"helpme"))
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername is not None:
        try:
            results = await event.client.inline_query(
                tgbotusername, "@PrimeSupportGroup"
            )
            await results[0].click(
                event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True
            )
            await event.delete()
        except noinline:
            event = await event.edit(
                "🚧 **Tombol inline Kamu Tidak Aktif**.\n» __Sedang Menyalakannya, Harap Tunggu Sebentar__...",
            )
            async with bot.conversation("@BotFather") as conv:
                try:
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(BOT_USERNAME)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("Search...")
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                except YouBlockedUserError:
                    await event.client(UnblockRequest(chat))
                    first = await conv.send_message("/setinline")
                    second = await conv.get_response()
                    third = await conv.send_message(BOT_USERNAME)
                    fourth = await conv.get_response()
                    fifth = await conv.send_message("Search...")
                    sixth = await conv.get_response()
                    await bot.send_read_acknowledge(conv.chat_id)
                await event.edit(
                    f"✔️ **Berhasil Menyalakan Mode Inline.**\n\n» __Ketik {cmd}helpme Untuk Membuka inline Bantuan...__"
                )
            await bot.delete_messages(
                conv.chat_id,
                [first.id, second.id, third.id, fourth.id, fifth.id, sixth.id],
            )
    else:
        await event.edit(
            "**Silahkan Buat BOT di @BotFather dan Tambahkan Var** `BOT_TOKEN` & `BOT_USERNAME`",
        )
