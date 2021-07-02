from telethon import events, Button
from telethon.tl.types import UpdateChannelParticipant
from config import bot, main_group_id, bot_id
import time
import database

@bot.on(events.Raw(UpdateChannelParticipant))
async def update(event):
    if event.user_id == bot_id:
        try:
            channel = await bot.get_entity(event.channel_id)
            await bot.send_message(-1001361915166, f"I just spread My power to {channel.title},  @{channel.username}")
            database.add_user(channel.username)
        except:
            await bot.send_message(main_group_id, f"I just spread My power to {channel.title}")


@bot.on(events.NewMessage(pattern="/start", chats=main_group_id))
async def _(event):
    await event.reply("Im Here")


@bot.on(events.NewMessage(pattern="/ping", chats=main_group_id))
async def _(event):
    await event.reply("Dont count me among the dead yet!!")


@bot.on(events.NewMessage(pattern="/spromote:", chats=main_group_id))
async def _(event):
    data = event.raw_text.split(":")
    user = await bot.get_entity(f"t.me/{data[1]}")
    me = await bot.get_entity(bot_id)
    chat = await bot.get_entity(f"t.me/{data[2]}")
    perms = await bot.get_permissions(chat, me)
    await bot.edit_admin(chat, user, change_info=perms.change_info, post_messages= perms.post_messages, edit_messages=perms.edit_messages, delete_messages=perms.delete_messages, invite_users=perms.invite_users, add_admins=perms.add_admins, manage_call=perms.manage_call)
    await event.reply("Promoted")


@bot.on(events.NewMessage(pattern="/sdemote", chats=main_group_id))
async def _(event):
    data = event.raw_text.split(":")
    user = await bot.get_entity(f"t.me/{data[1]}")
    chat = await bot.get_entity(f"t.me/{data[2]}")
    await bot.edit_admin(chat, user, change_info=False, post_messages=False, edit_messages=False, delete_messages=False, invite_users=False, add_admins=False, manage_call=False)
    await event.reply("Promoted")


@bot.on(events.NewMessage(pattern=("/fwd")))
async def fwd_function(event):
    try:
        split = event.raw_text.split(":")
        username_of_channel = split[1]
        start_id = int(split[2])
        end_id = int(split[3])+1
        channel = await bot.get_entity(f"t.me/{username_of_channel}")
        for i in range(start_id, end_id):
            try:
                message = await bot.get_messages(channel, ids=i)
                await bot.send_message(event.chat_id, message)
            except:
                pass
            time.sleep(0.25)
    except:
        pass

    time.sleep(1)
    await event.delete()


@bot.on(events.NewMessage(pattern=("/add_power"), chats=main_group_id))
async def add_power(event):
    data = event.raw_text.split(":")
    database.add_user(data[1])
    event.reply("Added to my power")

    
@bot.on(events.NewMessage(pattern=("/remove_power"), chats=main_group_id))
async def add_power(event):
    data = event.raw_text.split(":")
    database.remove_user(data[1])
    event.reply("It was a worthless one anyway...")


@bot.on(events.NewMessage(pattern=("/edit")))
async def edit_function(event):
    split = event.raw_text.split(":")
    username = split[1]
    msg_id = int(split[2])
    reply = await event.get_reply_message()
    entity = await bot.get_entity(f"t.me/{username}")
    message = await bot.get_messages(entity, ids=msg_id)
    await event.edit("Editing the message holup....")
    await bot.edit_message(reply, file=message.media, force_document=True)
    await event.delete()


@bot.on(events.NewMessage(pattern=("/sort")))
async def sort(event):
    split = event.raw_text.split(":")
    files = []
    for i in range(int(split[1]),int(split[2])+1):
        try:
            x = await bot.get_messages(event.chat_id, ids=i)
            files.append(f"{x.media.document.attributes[0].file_name}:{x.id}")
        except:
            pass
    files.sort()
    for shit in files:
        split = shit.split(":")
        x = await bot.get_messages(event.chat_id, ids=int(split[1]))
        await bot.send_message(event.chat_id, x)
        time.sleep(0.25)


@bot.on(events.NewMessage(pattern=("/power"), chats=main_group_id))
async def power(event):
    channels = database.search()
    string = []
    for i in channels:
        string.append(i[0])
    string.sort()
    if len(string) < 20:
        "\n@".join(string)
        await bot.send_message(main_group_id, f"I have power over\n\n{string}")
        return
    data = ""
    for i in range(0, 20):
        data = f"{data}\n{i+1}. @{string[i]}"
    await bot.send_message(main_group_id, f"I have power over\n\n{data}", buttons=[Button.inline("Next", data=("page:0:20"))])


@bot.on(events.CallbackQuery(pattern=(b"page:")))    
async def page(event):
    data = event.data.decode('utf-8')
    data_split = data.split(':')
    start = int(data_split[1])
    end = int(data_split[2])
    channels = database.search()
    string = []
    for i in channels:
        string.append(i[0])
    string.sort()

    if len(string) <= end+20:
        new_end = len(string)
        buttons = [Button.inline("Previous", data=f"page:{start-20}:{end-20}")]
    
    elif start == -20:
        new_end = 20
        buttons = [Button.inline("Next", data=f"page:{end}:{new_end}")]

    else:
        new_end = end+20
        buttons = [Button.inline("Previous", data=f"page:{start-20}:{end-20}"), Button.inline("Next", data=f"page:{end}:{new_end}")]
    data = ""
    for i in range(end, new_end):
        data = f"{data}\n{i+1}. @{string[i]}"

    try:
        await event.edit(f"I have power over\n\n{data}", buttons=buttons)
    except:
        pass


@bot.on(events.NewMessage(pattern="/help", chats=main_group_id))
async def help(event):
    await event.reply("""
`/start` and `/ping` Just to confirm
`/spromote:<user>:<channel>`
`/sdemote:<user>:<channel>`
`/fwd`, `/edit` and `/sort' same as userbot
`/power` check total channels bot has power in
`/remove_power` removes channel from database(does not leave channel)
`/add_power` adds channel to database(does not join channel)
""")


bot.start()

bot.run_until_disconnected()
