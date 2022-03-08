# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
    PeerChat,
)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, DEVS
from userbot.events import register, toni_cmd
from userbot import CMD_HANDLER as cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`Gambar Terlalu Kecil`"
PP_ERROR = "`Gagal Memproses Gambar`"
NO_ADMIN = "`Maaf Anda Bukan Admin:)`"
NO_PERM = "`Maaf Anda Tidak Mempunyai Izin!`"
NO_SQL = "`Berjalan Pada Mode Non-SQL`"

CHAT_PP_CHANGED = "`Berhasil Mengubah Profil Grup`"
CHAT_PP_ERROR = (
    "`Ada Masalah Dengan Memperbarui Foto,`"
    "`Mungkin Karna Anda Bukan Admin,`"
    "`Atau Tidak Mempunyai Izin.`"
)
INVALID_MEDIA = "`Media Tidak Valid`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


@toni_cmd(pattern="setgpic( -s| -d)$")
@register(pattern=r"^\.csetgpic( -s| -d)$")
async def set_group_photo(gpic):
    if not gpic.is_group:
        await gpic.edit("`Mohon Lakukan Perintah Ini Di Grup.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        return await gpic.edit(NO_ADMIN)

    if replymsg and replymsg.media:
        await gpic.edit("`Mengubah Profil Grup`")
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@toni_cmd(pattern="promote(?:\s|$)([\s\S]*)")
@register(pattern=r"^\.cpromote(?:\s|$)([\s\S]*)")
async def promote(promt):
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        return await promt.edit(NO_ADMIN)

    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    await promt.edit("`Promosikan Pengguna Sebagai Admin... Mohon Menunggu`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Admin"  # Just in case.
    if not user:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Berhasil Mempromosikan Pengguna Ini Sebagai Admin!`")
        await sleep(5)
        await promt.delete()

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        return await promt.edit(NO_PERM)

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOSI\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {promt.chat.title}(`{promt.chat_id}`)",
        )


@toni_cmd(pattern="demote(?:\s|$)([\s\S]*)")
@register(pattern=r"^\.cdemote(?:\s|$)([\s\S]*)")
async def demote(dmod):
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        return await dmod.edit(NO_ADMIN)

    # If passing, declare that we're going to demote
    await dmod.edit("`Sedang Melepas Admin...`")
    rank = "Admin"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        return await dmod.edit(NO_PERM)
    await dmod.edit("`Admin Berhasil Dilepas!`")
    await sleep(5)
    await dmod.delete()

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#MENURUNKAN\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@toni_cmd(pattern="ban(?:\s|$)([\s\S]*)")
@register(pattern=r"^\.cban(?:\s|$)([\s\S]*)")
async def ban(bon):
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await bon.edit(NO_ADMIN)

    user, reason = await get_user_from_event(bon)
    if not user:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Melakukan Banned!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await bon.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await bon.edit(
            "`Saya tidak memiliki hak pesan nuking! Tapi tetap saja dia di banned!`"
        )
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await bon.edit(
            f"`PENGGUNA:` [{user.first_name}](tg://user?id={user.id})\n`ID:` `{str(user.id)}` Telah Di Banned !!\n`Alasan:` {reason}"
        )
    else:
        await bon.edit(
            f"`PENGGUNA:` [{user.first_name}](tg://user?id={user.id})\n`ID:` `{str(user.id)}` Telah Di Banned !"
        )
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {bon.chat.title}(`{bon.chat_id}`)",
        )


@toni_cmd(pattern="unban(?:\s|$)([\s\S]*)")
@register(pattern=r"^\.cunban(?:\s|$)([\s\S]*)")
async def nothanos(unbon):
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await unbon.edit(NO_ADMIN)

    # If everything goes well...
    await unbon.edit("`Sedang Melakukan Unban...`")

    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return

    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Unban Berhasil Dilakukan!```")
        await sleep(3)
        await unbon.delete()

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await unbon.edit("`Sepertinya Terjadi Kesalahan!`")


@toni_cmd(pattern=r"mute(?: |$)(.*)")
@register(pattern=r"^\.cmute(?: |$)(.*)")
async def spider(spdr):
    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await spdr.edit(NO_SQL)

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await spdr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(spdr)
    if not user:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        return await spdr.edit(
            "`Tangan Terlalu Pendek, Tidak Bisa Membisukan Diri Sendiri...\n(ヘ･_･)ヘ┳━┳`"
        )

    # If everything goes well, do announcing and mute
    await spdr.edit("`Telah Dibisukan!`")
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit("`Error! Pengguna Sudah Dibisukan.`")
    else:
        try:
            await spdr.client(EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await spdr.edit(f"**Telah Dibisukan!**\n**Alasan:** `{reason}`")
            else:
                await spdr.edit("`Telah Dibisukan!`")

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID,
                    "#MUTE\n"
                    f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                    f"GRUP: {spdr.chat.title}(`{spdr.chat_id}`)",
                )
        except UserIdInvalidError:
            return await spdr.edit("`Terjadi Kesalahan!`")


@toni_cmd(pattern=r"unmute(?: |$)(.*)")
@register(pattern=r"^\.cunmute(?: |$)(.*)")
async def unmoot(unmot):
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await unmot.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await unmot.edit(NO_SQL)

    # If admin or creator, inform the user and start unmuting
    await unmot.edit("```Melakukan Unmute...```")
    user = await get_user_from_event(unmot)
    user = user[0]
    if not user:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`Kesalahan! Pengguna Sudah Tidak Dibisukan.`")
    else:

        try:
            await unmot.client(EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(
                "```Berhasil Melakukan Unmute! Pengguna Sudah Tidak Lagi Dibisukan```"
            )
            await sleep(3)
            await unmot.delete()
        except UserIdInvalidError:
            return await unmot.edit("`Terjadi Kesalahan!`")

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {unmot.chat.title}(`{unmot.chat_id}`)",
            )


@register(incoming=True)
async def muter(moot):
    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(
                    EditBannedRequest(moot.chat_id, moot.sender_id, rights)
                )
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@toni_cmd(pattern="ungmute(?: |$)(.*)")
@register(pattern=r"^\.cungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    # Admin or creator check
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await un_gmute.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except AttributeError:
        return await un_gmute.edit(NO_SQL)

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if not user:
        return

    # If pass, inform and start ungmuting
    await un_gmute.edit("```Membuka Global Mute Pengguna...```")

    if ungmute(user.id) is False:
        await un_gmute.edit("`Kesalahan! Pengguna Sedang Tidak Di Gmute.`")
    else:
        # Inform about success
        await un_gmute.edit("```Berhasil! Pengguna Sudah Tidak Lagi Dibisukan```")
        await sleep(3)
        await un_gmute.delete()

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)",
            )


@toni_cmd(pattern="gmute(?: |$)(.*)")
@register(pattern=r"^\.cgmute(?: |$)(.*)")
async def gspider(gspdr):
    # Admin or creator check
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await gspdr.edit(NO_ADMIN)

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except AttributeError:
        return await gspdr.edit(NO_SQL)

    user, reason = await get_user_from_event(gspdr)
    if not user:
        return

    # If pass, inform and start gmuting
    await gspdr.edit("`Berhasil Membisukan Pengguna!`")
    if gmute(user.id) is False:
        await gspdr.edit("`Kesalahan! Pengguna Sudah Dibisukan.`")
    else:
        if reason:
            await gspdr.edit(f"**Dibisukan Secara Global!**\n**Alasan:** `{reason}`")
        else:
            await gspdr.edit("`Berhasil Membisukan Pengguna Secara Global!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID,
                "#GLOBALMUTE\n"
                f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
                f"GRUP: {gspdr.chat.title}(`{gspdr.chat_id}`)",
            )


@toni_cmd(pattern="zombies(?: |$)(.*)")
async def rm_deletedacc(show):

    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`Tidak Menemukan Akun Terhapus, Grup Bersih`"

    if con != "clean":
        await show.edit("`Mencari Akun Hantu/Terhapus/Zombie...`")
        async for user in show.client.iter_participants(show.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"`Menemukan` **{del_u}** `Akun Hantu/Terhapus/Zombie Dalam Grup Ini,"
                "\nBersihkan Itu Menggunakan Perintah .zombies clean`"
            )
        return await show.edit(del_status)

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        return await show.edit("`Mohon Maaf, Bukan Admin Disini!`")

    await show.edit("`Menghapus Akun Terhapus...\nMohon Menunggu Sedang Dalam Proses`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS)
                )
            except ChatAdminRequiredError:
                return await show.edit("`Tidak Memiliki Izin Banned Dalam Grup Ini`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"`Membersihkan` **{del_u}** `Akun Terhapus`"

    if del_a > 0:
        del_status = (
            f"Membersihkan **{del_u}** Akun Terhapus "
            f"\n**{del_a}** `Admin Akun Terhapus Tidak Bisa Dihapus.`"
        )
    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            "#MEMBERSIHKAN\n"
            f"Membersihkan **{del_u}** Akun Terhapus!"
            f"\nGRUP: {show.chat.title}(`{show.chat_id}`)",
        )


@toni_cmd(pattern="admins$")
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title or "Grup Ini"
    mentions = f"<b>👑 Daftar Admin Grup {title}:</b> \n"
    try:
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n⚜️ {link}"
            else:
                mentions += f"\n⚜ Akun Terhapus <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")
    

@toni_cmd(pattern="pin( loud|$)")
@register(pattern=r"^\.cpin( loud|$)")
async def pin(event):
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "`Reply Pesan untuk Melakukan Pin.`", 30)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "`Pinned Successfully!`")
    
@toni_cmd(pattern="unpin( all|$)")
@register(pattern=r"^\.cunpin( all|$)")
async def pin(event):
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await edit_delete(
            event,
            "**Reply ke Pesan untuk melepas Pin atau Gunakan** `.unpin all` **untuk melepas pin semua**",
            45,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event,
                "**Reply ke Pesan untuk melepas pin atau gunakan** `.unpin all`",
                45,
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{e}`", 5)
    await edit_delete(event, "`Unpinned Successfully!`")


@toni_cmd(pattern="kick(?: |$)(.*)")
@register(pattern=r"^\.ckick(?: |$)(.*)")
async def kick(usr):
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        return await usr.edit(NO_ADMIN)

    user, reason = await get_user_from_event(usr)
    if not user:
        return await usr.edit("`Tidak Dapat Menemukan Pengguna.`")

    await usr.edit("`Melakukan Kick....`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        return await usr.edit(NO_PERM + f"\n{str(e)}")

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**\n**Alasan:** `{reason}`"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) **Telah Dikick Dari Grup**"
        )
        await sleep(5)
        await usr.delete()

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"PENGGUNA: [{user.first_name}](tg://user?id={user.id})\n"
            f"GRUP: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@toni_cmd(pattern=r"undlt( -u)?(?: |$)(\d*)?")
async def _iundlt(event):
    catevent = await edit_or_reply(event, "`Searching recent actions...`")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**{lim} Pesan yang dihapus di grup ini:**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n☞ __{msg.old.message}__ **Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n☞ __{_media_type}__ **Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(catevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(catevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**Dikirim oleh** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )


CMD_HELP.update(
    {
        "admin": f"**Plugin : **`admin`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}promote <username/reply> <nama title (optional)>`\
        \n  ↳ : **Mempromosikan member sebagai admin.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}demote <username/balas ke pesan>`\
        \n  ↳ : **Menurunkan admin sebagai member.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ban <username/balas ke pesan> <alasan (optional)>`\
        \n  ↳ : **Membanned Pengguna dari grup.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}unban <username/reply>`\
        \n  ↳ : **Unbanned pengguna jadi bisa join grup lagi.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}mute <username/reply> <alasan (optional)>`\
        \n  ↳ : **Membisukan Seseorang Di Grup, Bisa Ke Admin Juga.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}unmute <username/reply>`\
        \n  ↳ : **Membuka bisu orang yang dibisukan.\
        \n  ↳ : ** Membuka global mute orang yang dibisukan.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}all`\
        \n  ↳ : **Tag semua member dalam grup.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}admins`\
        \n  ↳ : **Melihat daftar admin di grup.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}setgpic <flags> <balas ke gambar>`\
        \n  ↳ : **Untuk mengubah foto profil grup atau menghapus gambar foto profil grup.\
        \n  •  **Flags :** `-s` = **Untuk mengubah foto grup** atau `-d` = **Untuk menghapus foto grup**\
    "
    }
)


CMD_HELP.update(
    {
        "pin": f"**Plugin : **`pin`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}pin` <reply chat>\
        \n  ↳ : **Untuk menyematkan pesan dalam grup.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}pin loud` <reply chat>\
        \n  ↳ : **Untuk menyematkan pesan dalam grup (tanpa notifikasi) / menyematkan secara diam diam.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}unpin` <reply chat>\
        \n  ↳ : **Untuk melepaskan pin pesan dalam grup.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}unpin all`\
        \n  ↳ : **Untuk melepaskan semua sematan pesan dalam grup.\
    "
    }
)


CMD_HELP.update(
    {
        "undelete": f"**Plugin : **`undelete`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}undlt` <jumlah chat>\
        \n  ↳ : **Untuk mendapatkan pesan yang dihapus baru-baru ini di grup\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}undlt -u` <jumlah chat>\
        \n  ↳ : **Untuk mendapatkan pesan media yang dihapus baru-baru ini di grup \
        \n  •  **Flags :** `-u` = **Gunakan flags ini untuk mengunggah media.**\
        \n\n  •  **NOTE : Membutuhkan Hak admin Grup** \
    "
    }
)


CMD_HELP.update(
    {
        "gmute": f"**Plugin : **`gmute`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}gmute` <username/reply> <alasan (optional)>\
        \n  ↳ : **Untuk Membisukan Pengguna di semua grup yang kamu admin.\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}ungmute` <username/reply>\
        \n  ↳ : **Untuk Membuka global mute Pengguna di semua grup yang kamu admin.\
    "
    }
)


CMD_HELP.update(
    {
        "zombies": f"**Plugin : **`zombies`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}zombies`\
        \n  ↳ : **Untuk mencari akun terhapus dalam grup\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `{cmd}zombies clean`\
        \n  ↳ : **untuk menghapus Akun Terhapus dari grup.\
    "
    }
)
