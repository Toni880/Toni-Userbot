# Credits: mrconfused
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from userbot import (
  CMD_HANDLER as cmd,
  BOTLOG_CHATID,
  CMD_HELP,
  LOGS,
)
from userbot.modules.sql_helper import no_log_pms_sql
from userbot.modules.sql_helper.globals import addgvar, gvarstatus
from userbot.modules.vcplugin import vcmention
from userbot.utils import (
    _format,
    chataction,
    edit_delete,
    edit_or_reply,
    toni_cmd,
    toni_handler,
)
from userbot.utils.tools import media_type


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@chataction()
async def logaddjoin(toni):
    user = await toni.get_user()
    chat = await toni.get_chat()
    if not (user and user.is_self):
        return
    if hasattr(chat, "username") and chat.username:
        chat = f"[{chat.title}](https://t.me/{chat.username}/{toni.action_message.id})"
    else:
        chat = f"[{chat.title}](https://t.me/c/{chat.id}/{toni.action_message.id})"
    if toni.user_added:
        tmp = toni.added_by
        text = f"📩 **#ADD_LOG\n •** {vcmention(tmp)} **Menambahkan** {vcmention(user)}\n **• Ke Group** {chat}"
    elif toni.user_joined:
        text = f"📨 **#JOIN_LOG\n •** [{user.first_name}](tg://user?id={user.id}) **Bergabung\n • Ke Group** {chat}"
    else:
        return
    await toni.client.send_message(BOTLOG_CHATID, text)


@toni_handler(incoming=True, func=lambda e: e.is_private)
async def monito_p_m_s(toni):
    if BOTLOG_CHATID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await toni.get_sender()
    await asyncio.sleep(0.5)
    if not sender.bot:
        chat = await toni.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    await LOG_CHATS_.NEWPM.edit(
                        LOG_CHATS_.NEWPM.text.replace(
                            "**💌 #NEW_MESSAGE**",
                            f" • `{LOG_CHATS_.COUNT}` **Pesan**",
                        )
                    )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await toni.client.send_message(
                    BOTLOG_CHATID,
                    f"**💌 #MENERUSKAN #PESAN_BARU**\n** • Dari : **{_format.mentionuser(sender.first_name , sender.id)}\n** • User ID:** `{chat.id}`",
                )
            try:
                if toni.message:
                    await toni.client.forward_messages(
                        BOTLOG_CHATID, toni.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@toni_handler(incoming=True, func=lambda e: e.mentioned)
async def log_tagged_messages(toni):
    if BOTLOG_CHATID == -100:
        return
    hmm = await toni.get_chat()

    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (BOTLOG_CHATID == -100)
        or (await toni.get_sender() and (await toni.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await toni.client.get_entity(toni.message.sender_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(toni)
    resalt = f"<b>📨 #TAGS #MESSAGE</b>\n<b> • Dari : </b>{_format.htmlmentionuser(full.first_name , full.id)}"
    if full is not None:
        resalt += f"\n<b> • Grup : </b><code>{hmm.title}</code>"
    if messaget is not None:
        resalt += f"\n<b> • Jenis Pesan : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b> • 👀 </b><a href = 'https://t.me/c/{hmm.id}/{toni.message.id}'>Lihat Pesan</a>"
    resalt += f"\n<b> • Message : </b>{toni.message.message}"
    await asyncio.sleep(0.5)
    if not toni.is_private:
        await toni.client.send_message(
            BOTLOG_CHATID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@toni_cmd(pattern="save(?: |$)(.*)")
async def log(log_text):
    if BOTLOG_CHATID:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"**#LOG / Chat ID:** {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await log_text.client.send_message(BOTLOG_CHATID, textx)
        else:
            await edit_delete(log_text, "**Apa yang harus saya simpan?**")
            return
        await edit_delete(log_text, "**Berhasil disimpan di Grup Log**")
    else:
        await edit_delete(
            log_text,
            "**Untuk Menggunakan Module ini, Anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**",
            30,
        )


@toni_cmd(pattern="log$")
async def set_log_p_m(toni):
    if BOTLOG_CHATID != -100:
        chat = await toni.get_chat()
        if no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.disapprove(chat.id)
            await edit_delete(
                toni, "**LOG Chat dari Grup ini Berhasil Diaktifkan**", 15
            )


@toni_cmd(pattern="nolog$")
async def set_no_log_p_m(toni):
    if BOTLOG_CHATID != -100:
        chat = await toni.get_chat()
        if not no_log_pms_sql.is_approved(chat.id):
            no_log_pms_sql.approve(chat.id)
            await edit_delete(
                toni, "**LOG Chat dari Grup ini Berhasil Dimatikan**", 15
            )


@toni_cmd(pattern="pmlog (on|off)$", allow_sudo=False)
async def set_pmlog(toni):
    if BOTLOG_CHATID == -100:
        return await edit_delete(
            toni,
            "**Untuk Menggunakan Module ini, Anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**",
            30,
        )
    input_str = toni.pattern_match.group(1)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await edit_or_reply(toni, "**PM LOG Sudah Diaktifkan**")
        else:
            addgvar("PMLOG", h_type)
            await edit_or_reply(toni, "**PM LOG Berhasil Dimatikan**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await edit_or_reply(toni, "**PM LOG Berhasil Diaktifkan**")
    else:
        await edit_or_reply(toni, "**PM LOG Sudah Dimatikan**")


@toni_cmd(pattern="gruplog (on|off)$")
async def set_gruplog(toni):
    if BOTLOG_CHATID == -100:
        return await edit_delete(
            toni,
            "**Untuk Menggunakan Module ini, Anda Harus Mengatur** `BOTLOG_CHATID` **di Config Vars**",
            30,
        )
    input_str = toni.pattern_match.group(1)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("GRUPLOG") and gvarstatus("GRUPLOG") == "false":
        GRUPLOG = False
    else:
        GRUPLOG = True
    if GRUPLOG:
        if h_type:
            await edit_or_reply(toni, "**Group Log Sudah Diaktifkan**")
        else:
            addgvar("GRUPLOG", h_type)
            await edit_or_reply(toni, "**Group Log Berhasil Dimatikan**")
    elif h_type:
        addgvar("GRUPLOG", h_type)
        await edit_or_reply(toni, "**Group Log Berhasil Diaktifkan**")
    else:
        await edit_or_reply(toni, "**Group Log Sudah Dimatikan**")


CMD_HELP.update(
    {
        "logger": f"**Plugin : **`logger`\
        \n\n  •  **Syntax :** `{cmd}save`\
        \n  •  **Function : **__Untuk Menyimpan pesan yang ditandai ke grup pribadi.__\
        \n\n  •  **Syntax :** `{cmd}log`\
        \n  •  **Function : **__Untuk mengaktifkan Log Chat dari obrolan/grup itu.__\
        \n\n  •  **Syntax :** `{cmd}nolog`\
        \n  •  **Function : **__Untuk menonaktifkan Log Chat dari obrolan/grup itu.__\
        \n\n  •  **Syntax :** `{cmd}pmlog on/off`\
        \n  •  **Function : **__Untuk mengaktifkan atau menonaktifkan pencatatan pesan pribadi__\
        \n\n  •  **Syntax :** `{cmd}gruplog on/off`\
        \n  •  **Function : **__Untuk mengaktifkan atau menonaktifkan tag grup, yang akan masuk ke grup pmlogger.__"
    }
)
