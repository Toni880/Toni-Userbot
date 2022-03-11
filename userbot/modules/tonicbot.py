from time import sleep

from userbot import CMD_HELP, CMD_HANDLER as cmd
from userbot.utils import toni_cmd, edit_or_reply


@toni_cmd(pattern="sadboy(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    sleep(2)
    sad = await edit_or_reply(typew, "`Pertama-tama kamu cantik`")
    sleep(2)
    await sad.edit("`Kedua kamu manis`")
    sleep(1)
    await sad.edit("`Dan yang terakhir adalah kamu bukan jodohku`")


# Create by myself @localheart
@toni_cmd(pattern="lahk(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    lah = await edit_or_reply(typew, "`Lahk, Lo tolol?`")
    sleep(1)
    await lah.edit("`Apa dongok?`")
    sleep(1)
    await lah.edit("`Gausah sok keras`")
    sleep(1)
    await lah.edit("`Gua ga ketrigger sama bocah baru nyemplung!`")


@toni_cmd(pattern="wah(?: |$)(.*)")
async def typewriter(typew):
    typew.pattern_match.group(1)
    wah = await edit_or_reply(typew, "`Wahh, War nya keren bang`")
    sleep(2)
    await wah.edit("`Tapi, Yang gua liat, kok Kaya lawakan`")
    sleep(2)
    await wah.edit("`Oh iya, Kan lo badut 🤡`")
    sleep(2)
    await wah.edit("`Kosa kata pas ngelawak, Jangan di pake war bang`")
    sleep(2)
    await wah.edit("`Kesannya lo ngasih kita hiburan.`")
    sleep(2)
    await wah.edit(
        "`Kasian badut🤡, Ga di hargain pengunjung, Eh lampiaskan nya ke Tele, Wkwkwk`"
    )
    sleep(3)
    await wah.edit("`Dah sana cabut, Makasih hiburannya, Udah bikin Gua tawa ngakak`")


CMD_HELP.update(
    {
    "tonicubot": f"𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{cmd}sadboy`\
    \n↳ : Biasalah sadboy hikss\
    \n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{cmd}wah`\
    \n↳ : Ngatain orang war\
    \n\n𝘾𝙤𝙢𝙢𝙖𝙣𝙙: `{cmd}lahk`\
    \n↳ : Ngatain orang sok keras.\."
}
)
