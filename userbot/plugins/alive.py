Import datetime
Import random
Import time

From telethon.errors import ChatSendInlineForbiddenError as noin
From telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

From . import *

#-------------------------------------------------------------------------------

ALIVE_TEMP = “””
<b><i>🔥🔥EAGLEMAFIA-USPAMBOT 🔥🔥</b></i>
<i><b>↼ Øwñêr ⇀</i></b> : 『 <a href=’tg://user?id={}’>{}</a> 』
╭──────────────
┣─ <b>» Telethon ~</b> <i>{}</i>
┣─ <b>» 𝔐𝔞𝔣𝔦𝔞 𝔰𝔭𝔞𝔪 𝔟𝔬𝔱 ~</b> <i>{}</i>
┣─ <b>» Sudo ~</b> <i>{}</i>
┣─ <b>» Uptime ~</b> <i>{}</i>
┣─ <b>» Ping ~</b> <i>{}</i>
╰──────────────
<b><i>»»» <a href=’https://t.me/its_userbot'>[ 𝔐𝔞𝔣𝔦𝔞 𝔖𝔭𝔞𝔪 𝔟𝔬𝔱 ]</a> «««</i></b>
“””
#-------------------------------------------------------------------------------

@userbot_cmd(pattern=”alive$”)
Async def up(event):
    cid = await client_id(event)
    ForGo10God, USERBOT_USER, userbot_mention = cid[0], cid[1], cid[2]
    Start = datetime.datetime.now()
    Userbot = await eor(event, “`Building Alive....`”)
    Uptime = await get_time((time.time() – StartTime))
    A = gvarstat(“ALIVE_PIC”)
    If a is not None:
        B = a.split(“ “)
        C = []
        If len(b) >= 1:
            For d in b:
                c.append(d)
        PIC = random.choice(c)
    Else:
        PIC = 
    Userbot_pic = PIC
    End = datetime.datetime.now()
    Ling = (end – start).microseconds / 1000
    Omk = ALIVE_TEMP.format(ForGo10God, USERBOT_USER, tel_ver, userbot_ver, is_sudo, uptime, ling)
    Await event.client.send_file(event.chat_id, file=userbot_pic, caption=omk, parse_mode=”HTML”)
    Await userbot.delete()


Msg = “””{}\n
<b><i>🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>spam bot≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Abuse ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
“””
Botname = Config.BOT_USERNAME

@userbot_cmd(pattern=”userbot$”)
Async def userbot_a(event):
    cid = await client_id(event)
    ForGo10God, USERBOT_USER, userbot_mention = cid[0], cid[1], cid[2]
    Uptime = await get_time((time.time() – StartTime))
    Am = gvarstat(“ALIVE_MSG”) or “<b>»» Mafia spam bot ιѕ σиℓιиє ««</b>”
    Try:
        Userbot = await event.client.inline_query(botname, “alive”)
        Await userbot[0].click(event.chat_id)
        If event.sender_id == ForGo10God:
            Await event.delete()
    Except (noin, dedbot):
        Await eor(event, msg.format(am, tel_ver, userbot_ver, uptime, abuse_m, is_sudo), parse_mode=”HTML”)


CmdHelp(“alive”).add_command(
  “alive”, None, “Shows the Default Alive Message”
).add_command(
  “userbot”, None, “Shows Inline Alive Menu with more details.”
).add_warning(
  “✅ Harmless Module”
).add()
