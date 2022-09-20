import os

from telethon.errors import ChatAdminRequiredError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.users import GetFullUserRequest

from ..utils import admin_cmd , sudo_cmd
from . import ALIVE_NAME

naam = str(ALIVE_NAME)

bots = "@MissRose_bot"

BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

G_BAN_LOGGER_GROUP = os.environ.get("G_BAN_LOGGER_GROUP", None)
if G_BAN_LOGGER_GROUP:
    G_BAN_LOGGER_GROUP = int(G_BAN_LOGGER_GROUP)


@bot.on(admin_cmd("fstat ?(.*)"))
@bot.on(sudo_cmd("fstat ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        sysarg = event.pattern_match.group(1)
    else:
        sysarg = ""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        getuser = str(replied_user.user.id)
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + getuser + " " + sysarg)
                fedstat = await conv.get_response()
                if "file" in fedstat.text:
                    await fedstat.click(0)
                    reply = await conv.get_response()
                    await event.client.forward_messages(event.chat_id, reply)
                else:
                    await event.client.forward_messages(event.chat_id, fedstat)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_bot `and retry!")
    else:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + sysarg)
                fedstat = await conv.get_response()
                if "file" in fedstat.text:
                    await fedstat.click(0)
                    reply = await conv.get_response()
                    await event.client.forward_messages(event.chat_id, reply)
                else:
                    await event.client.forward_messages(event.chat_id, fedstat)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd("info ?(.*)"))
@bot.on(sudo_cmd("info ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        sysarg = event.pattern_match.group(1)
    else:
        sysarg = ""
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.sender_id)
        )
        getuser = str(replied_user.user.id)
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/info " + getuser)
                audio = await conv.get_response()
                await event.client.forward_messages(event.chat_id, audio)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_bot `and retry!")
    else:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/info " + sysarg)
                audio = await conv.get_response()
                await event.client.forward_messages(event.chat_id, audio)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd("fedinfo ?(.*)"))
@bot.on(sudo_cmd("fedinfo ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    sysarg = event.pattern_match.group(1)
    if sysarg == "" and not event.reply_to_msg_id:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedinfo")
                fedinfo = await conv.get_response()
                await event.client.forward_messages(event.chat_id, fedinfo)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_bot `and retry!")
    else:
        async with event.client.conversation(bots) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedinfo " + sysarg)
                fedinfo = await conv.get_response()
                await event.client.forward_messages(event.chat_id, fedinfo)
                await event.delete()
            except YouBlockedUserError:
                await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd("feds ?(.*)"))
@bot.on(sudo_cmd("feds ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    async with event.client.conversation(bots) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/myfeds")
            myfed = await conv.get_response()
            if "file" in myfed.text:
                await myfed.click(0)
                reply = await conv.get_response()
                await event.client.forward_messages(event.chat_id, reply)
            else:
                await event.client.forward_messages(event.chat_id, myfed)
                await event.delete()
        except YouBlockedUserError:
            await event.edit("**Error:** `unblock` @MissRose_Bot `and try again!")


@bot.on(admin_cmd(pattern=r"fsn ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"fsn ?(.*)", allow_sudo=True))
async def get_users(show):
    await show.delete()
    if not show.text[0].isalpha() and show.text[0] not in ("/"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "id,reason"
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},⚠️🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW"
                        "\nBAN CODES"
"\n"
"\n{TBH×000} - TOXIC"
"\n"
"\n{TBH×001} - SCAMMER"
"\n"
"\n{TBH×006} - PUTTING FAKE ALLEGATIONS"
"\n"
"\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS"
"\n"
"\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS"
"\n"
"\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC."
"\n"
"\n{TBH×025} - ABUSING GIRLS IN DM."
"\n"
"\n{TBH×026} - ASKING FOR SEX CHAT"
"\n"
"\nProofs :-"
"\n"
"\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg"
"\n"
"\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg"
"\n"
"\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg"
"\n"
"\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg"
"\n"
"\nOFFICIALLY BANNED BY "
"\n"
"\n@THE_BROTHERHOOD_COUNCIL "
"\n"
"\n#FEEL_THE_POWER_OF_BROTHERHOOD "
"\n"
"\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(
                    show.chat_id, search=f"{searchq}"
                ):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        file = open("userslist.csv", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            BOTLOG_CHATID,
            "userslist.csv",
            caption="Group Members in {}".format(title),
            reply_to=show.id,
        )


@bot.on(admin_cmd(pattern=r"tfn ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=r"tfn ?(.*)", allow_sudo=True))
async def get_users(show):
    await show.delete()
    if not show.text[0].isalpha() and show.text[0] not in ("/"):
        if not show.is_group:
            await show.edit("Are you sure this is a group?")
            return
        info = await show.client.get_entity(show.chat_id)
        title = info.title if info.title else "this chat"
        mentions = "id,reason"
        try:
            if not show.pattern_match.group(1):
                async for user in show.client.iter_participants(show.chat_id):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
            else:
                searchq = show.pattern_match.group(1)
                async for user in show.client.iter_participants(
                    show.chat_id, search=f"{searchq}"
                ):
                    if not user.deleted and user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
                    elif user.id != bot.uid:
                        mentions += f"\n{user.id},🚫🚫THIS NIGGA IS AN TOXIC. SO NIGGA NOW I WILL REMOVE TOXICITY FROM YOUR SOUL JUST WAIT & WATCH THE SHOW🚫🚫
                        \nBAN CODES :- 
\n
\n{TBH×000} - TOXIC
\n
\n{TBH×001} - SCAMMER
\n
\n{TBH×006} - PUTTING FAKE ALLEGATIONS
\n
\n{TBH×012} - MISUSE OF FEDADMIN RIGHTS/ GIVING FAKE FBANS
\n
\n{TBH×013} - MAKING FAKE FEDS AND GIVING FAKE FBANS
\n
\n{TBH×023} - LEAKING PRIVACY PIC NUMBER ETC.
\n
\n{TBH×025} - ABUSING GIRLS IN DM.
\n
\n{TBH×026} - ASKING FOR SEX CHAT
\n
\nProofs :-
\n
\nhttps://te.legra.ph/file/5666ffe23b36b0156b9e0.jpg
\n
\nhttps://te.legra.ph/file/8f8657e28f8014faf261f.jpg
\n
\nhttps://te.legra.ph/file/b2f3f5f080bcb8e5dd000.jpg
\n
\nhttps://te.legra.ph/file/5b1631694a5aca0d8a321.jpg
\n
\nOFFICIALLY BANNED BY 
\n
\n@THE_BROTHERHOOD_COUNCIL 
\n
\n#FEEL_THE_POWER_OF_BROTHERHOOD 
\n
\n#𝐅𝐄𝐄𝐋_𝐓𝐇𝐄_𝐏𝐎𝐖𝐄𝐑_𝐎𝐅_𝐂𝐋𝐀𝐍🔞🛑"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        file = open("userslist.csv", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            BOTLOG_CHATID,
            "userslist.csv",
            caption="Group Members in {}".format(title),
            reply_to=show.id,
        )




import asyncio

#  (c)2020 Telebot
#
# You may not use this plugin without proper authorship and consent from @TelebotSupport
#
import os

FBAN_GROUP_ID = os.environ.get("FBAN_GROUP_ID", None)
if FBAN_GROUP_ID:
    FBAN_GROUP_ID = int(FBAN_GROUP_ID)
EXCLUDE_FED = os.environ.get("EXCLUDE_FED", None)

# By @HeisenbergTheDanger, @its_xditya
@bot.on(admin_cmd("superfban ?(.*)"))
@bot.on(sudo_cmd("superfban ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting a Mass-FedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message, "fedlist"
            )
            await asyncio.sleep(6)
            file = open(downloaded_file_name, "r")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except:
                    pass
            arg = event.text.split(" ", maxsplit=2)
            if len(arg) > 2:
                FBAN = arg[1]
                REASON = arg[2]
            else:
                FBAN = arg[1]
                REASON = " #MassBanned "
        else:
            FBAN = previous_message.sender_id
            REASON = event.text.split(" ", maxsplit=1)[1]
            if REASON.strip() == "":
                REASON = " #MassBanned "
    else:
        arg = event.text.split(" ", maxsplit=2)
        if len(arg) > 2:
            FBAN = arg[1]
            REASON = arg[2]
        else:
            FBAN = arg[1]
            REASON = " #MassBanned "
    try:
        int(FBAN)
        if int(FBAN) == 1118936839 or int(FBAN) == 630654925 or int(FBAN) == 719195224:
            await event.edit("Something went wrong.")
            return
    except:
        if (
            FBAN == "@Surv_ivor"
            or FBAN == "@Sur_ivor"
            or FBAN == "@HeisenbergTheDanger"
            or FBAN == "@xditya"
        ):
            await event.edit("Something went wrong.")
            return
    if FBAN_GROUP_ID:
        chat = FBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with event.client.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                response = await bot_conv.get_response()
                await asyncio.sleep(3)
                if "make a file" in response.text:
                    await asyncio.sleep(6)
                    await response.click(0)
                    await asyncio.sleep(6)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await event.client.download_media(
                            fedfile, "fedlist"
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, "r")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except:
                                pass
                    else:
                        return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
        else:
            await event.edit(f"Error")
        if "You can only use fed commands once every 5 minutes" in response.text:
            await event.edit("Try again after 5 mins.")
            return
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True

            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await event.edit("Something went wrong.")
            return
    await event.edit(f"Fbaning in {len(fedList)} feds.")
    try:
        await event.client.send_message(chat, f"/start")
    except:
        await event.edit("FBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    if EXCLUDE_FED:
        excludeFed = EXCLUDE_FED.split("|")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if EXCLUDE_FED and fed in excludeFed:
            await event.client.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await event.client.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await event.client.send_message(chat, f"/fban {FBAN} {REASON}")
        await asyncio.sleep(3)
    await event.edit(f"SuperFBan Completed. Affected {len(fedList) - exCount} feds.")


# By @HeisenbergTheDanger, @its_xditya
@bot.on(admin_cmd("superunfban ?(.*)"))
@bot.on(sudo_cmd("superunfban ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting a Mass-UnFedBan...")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        FBAN = previous_message.sender_id
    else:
        FBAN = event.pattern_match.group(1)

    if FBAN_GROUP_ID:
        chat = FBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    fedList = []
    for a in range(3):
        async with event.client.conversation("@MissRose_bot") as bot_conv:
            await bot_conv.send_message("/start")
            await bot_conv.send_message("/myfeds")
            response = await bot_conv.get_response()
            if "make a file" in response.text:
                await asyncio.sleep(1)
                await response.click(0)
                fedfile = await bot_conv.get_response()
                if fedfile.media:
                    downloaded_file_name = await event.client.download_media(
                        fedfile, "fedlist"
                    )
                    file = open(downloaded_file_name, "r")
                    lines = file.readlines()
                    for line in lines:
                        fedList.append(line[:36])
                else:
                    return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
    else:
        await event.edit(f"Error")
    if "You can only use fed commands once every 5 minutes" in response.text:
        await event.edit("Try again after 5 mins.")
        return
    In = False
    tempFedId = ""
    for x in response.text:
        if x == "`":
            if In:
                In = False
                fedList.append(tempFedId)
                tempFedId = ""
            else:
                In = True

        elif In:
            tempFedId += x

    await event.edit(f"UnFbaning in {len(fedList)} feds.")
    try:
        await event.client.send_message(chat, f"/start")
    except:
        await event.edit("FBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    for fed in fedList:
        await event.client.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await event.client.send_message(chat, f"/unfban {FBAN}")
        await asyncio.sleep(3)
    await event.edit(f"SuperUnFBan Completed. Affected {len(fedList)} feds.")
