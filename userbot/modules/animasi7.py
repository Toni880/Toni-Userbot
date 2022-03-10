# Ported by @Pocongonlen
# From Pocong-Userbot <https://github.com/poocong/Pocong-Userbot>
# Recode by @greyyvbss


from time import sleep
from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_or_reply, toni_cmd


@toni_cmd(pattern="hai(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**Hai ,  Assalamualaikum**")
    sleep(1)
    await xx.edit("Kalian Nungguin aku gak??")
    sleep(1)
    await xx.edit("Ih ga mau🤢")
    sleep(1)
    await xx.edit("gasukaa😫")
    sleep(1)
    await xx.edit("__GELAYY__🤮")    
   

@toni_cmd(pattern="kntl(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"Tau kh kalian wahai tuan-tuan??")
    sleep(1)
    await xx.edit("se**KONT0L** **K0NTOL** nya si **K0NTOL**")
    sleep(1)
    await xx.edit("lebih **KONTOL** lagi")              
    sleep(1)
    await xx.edit("kalian")
    await xx.edit("kalian **K**")
    await xx.edit("kalian **Ko**")
    await xx.edit("kalian **Kon**")
    await xx.edit("kalian **Kont**")
    await xx.edit("kalian **Konto**")
    await xx.edit("kalian **Kontol**")


@toni_cmd(pattern="Phe(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**ga usah sok keras deh bg**")
    sleep(2)
    await xx.edit("**karena lu petinggi di tele**")
    sleep(1)
    await xx.edit("**atau karena title lu itu**")
    sleep(1)
    await xx.edit("**ga ngaruh di rl bg.**")    


@toni_cmd(pattern="phe(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"**ga usah sok keras deh bg**")
    sleep(2)
    await xx.edit("**karena lu petinggi di tele**")
    sleep(1)
    await xx.edit("**atau karena title lu itu**")
    sleep(1)
    await xx.edit("**ga ngaruh di rl bg**")
    
    
@toni_cmd(pattern="alay(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"eh kamu, iya kamu")
    sleep(1)
    await xx.edit("**ALAY** bnget sih")
    sleep(1)
    await xx.edit("spam bot mulu")
    sleep(1)
    await xx.edit("baru jadi userbot ya?? xixixi")
    sleep(1)
    await xx.edit("pantes **NORAK**")
    
@toni_cmd(pattern="jawa(?: |$)(.*)")
async def _(event):
    xx = await edit_or_reply(event, f"baik")
    sleep(1)
    await xx.edit("Tidak Sombong")
    sleep(1)
    await xx.edit("Ganteng")
    sleep(1)
    await xx.edit("Sopan")
    sleep(1)
    await xx.edit("Rajin")
    sleep(1)
    await xx.edit("Budiman")
    sleep(1)
    await xx.edit("Alim")
    sleep(1)
    await xx.edit("Berguna")
    sleep(1)
    await xx.edit("**Nguli Juga**")
    sleep(1)
    await xx.edit("Pemaaf")
    sleep(1)
    await xx.edit("Jujur")
    sleep(1)
    await xx.edit("Tidk Sombong")
    sleep(1)
    await xx.edit("Kaya")
    sleep(1)
    await xx.edit("Pokoknya Jawa Pro Dah")
    sleep(1)
    await xx.edit("Tidak Seperti Yang Lain")
    sleep(1)
    await xx.edit("Bersama Kuli Membangun Negri")
    sleep(1)
    await xx.edit("eh salah salah, \nBersama **Jawa** Membangun Negri")
    
    
CMD_HELP.update(
    {
    "animasi1": f"**Perintah**: **animasi8**\
    \n**Total Command: 6**\
    \n\nㅤㅤ•**Syntax**: {cmd}hai\
    \n•**Function**: __Cosplay Nissa Sablon__\
    \n\nㅤㅤ•**Syntax**: {cmd}kntl\
    \n•**Function**: __Kalian kntl__\
    \n\nㅤㅤ•**Syntax**: {cmd}alay\
    \n•**Function**: __Lumayanlah Buat Nyindir__\
    \n\nㅤㅤ•**Syntax**: {cmd}phe / {cmd}Phe\
    \n•**Function**: __Jagoan tele__\
    \n\nㅤㅤ•**Syntax**: {cmd}ehm\
    \n•**Function**: __Eum Biasalah cewe mau nya call mulu__\
    \n\nㅤㅤ•**Syntax**: {cmd}lopu\
    \n•**Function**: __Nyatakan Cinta Ke Cewe Orng__\
    \n\nㅤㅤ•**Syntax**: {cmd}dahlah\
    \n•**Function**: __Cek Aja dh sndri__\
    \n\nㅤㅤ•**Syntax**: {cmd}jawa\
    \n•**Function**: __Jawa Pride Ni Bos.__"

   
})
