""" Userbot module for other small commands. """
from userbot import ALIVE_NAME, CMD_HELP, CMD_HANDLER as cmd
from userbot.utils import toni_cmd

@toni_cmd(pattern="lhelp$")
async def usit(e):
    await e.edit(
        f"**Halo {ALIVE_NAME} Jika Anda Tidak Tau Perintah Untuk Memerintah Ku Ketik** `{cmd}help` Atau Bisa Minta Bantuan Ke:\n"
        "\n[Telegram](t.me/Bukan_guudlooking)"
        "\n[Repo](https://github.com/Tonic990/Tonic-UserBot)"
    )


@toni_cmd(pattern="vars$")
async def var(m):
    await m.edit(
        f"**Disini Daftar Vars Dari {ALIVE_NAME}:**\n"
        "\n[DAFTAR VARS](https://raw.githubusercontent.com/SendiAp/Rose-Userbot/Rose-Userbot/varshelper.txt)"
    )


CMD_HELP.update(
    {
        "helper": f"`{cmd}lhelp`\
\nUsage: Bantuan Untuk Tonic-Userbot.\
\n`{cmd}vars`\
\nUsage: Melihat Daftar Vars."
    }
)
