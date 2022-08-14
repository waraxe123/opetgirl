from telethon import events, Button, custom, version
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import os, re
import requests
import datetime
import time
from datetime import datetime
import random
from PIL import Image
from io import BytesIO
from CatXGirl import telethn as bot
from CatXGirl import telethn as tgbot
from CatXGirl.events import register
from CatXGirl import dispatcher


edit_time = 5
""" =======================CatxGirlT====================== """
file1 = "https://telegra.ph/file/e92d6e9307c341661a50a.jpg"
file2 = "https://telegra.ph/file/db981389e5f6d1ac73e3d.jpg"
file3 = "https://telegra.ph/file/97888764855f1c7ac9e5b.jpg"
file4 = "https://telegra.ph/file/ed1ce7fee94f46b0f671e.jpg"
file5 = "https://telegra.ph/file/701028ce085ecfa961a36.jpg"
""" =======================CatXGirl====================== """


@register(pattern="/myinfo")
async def proboyx(event):
    chat = await event.get_chat()
    current_time = datetime.utcnow()
    firstname = event.sender.first_name
    button = [[custom.Button.inline("information", data="informations")]]
    on = await bot.send_file(
        event.chat_id,
        file=file2,
        caption=f"Hey {firstname}, \n Click on the button below \n to get info about you",
        buttons=button,
    )

    await asyncio.sleep(edit_time)
    ok = await bot.edit_message(event.chat_id, on, file=file3, buttons=button)

    await asyncio.sleep(edit_time)
    ok2 = await bot.edit_message(event.chat_id, ok, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok3 = await bot.edit_message(event.chat_id, ok2, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)

    await asyncio.sleep(edit_time)
    ok4 = await bot.edit_message(event.chat_id, ok3, file=file2, buttons=button)

    await asyncio.sleep(edit_time)
    ok5 = await bot.edit_message(event.chat_id, ok4, file=file1, buttons=button)

    await asyncio.sleep(edit_time)
    ok6 = await bot.edit_message(event.chat_id, ok5, file=file3, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file5, buttons=button)

    await asyncio.sleep(edit_time)
    ok7 = await bot.edit_message(event.chat_id, ok6, file=file4, buttons=button)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"information")))
async def callback_query_handler(event):
    try:
        boy = event.sender_id
        PRO = await bot.get_entity(boy)
        LILIE = "POWERED BY ImRishmika \n\n"
        LILIE += f"FIRST NAME : </ Rishmika Sandanu[SL]/> \n"
        LILIE += f"LAST NAME : Not Found\n"
        LILIE += f"YOU BOT : @ImRishmika_Bot \n"
        LILIE += f"RESTRICTED : Not Found \n"
        LILIE += f"USER ID : 5171347305\n"
        LILIE += f"USERNAME : @ImRishmika\n"
        await event.answer(LILIE, alert=True)
    except Exception as e:
        await event.reply(f"{e}")


__command_list__ = ["myinfo"]
