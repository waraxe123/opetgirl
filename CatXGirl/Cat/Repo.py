from CatXGirl import app

from CatXGirl.cat.commands import *

@app.on_message(command("#Repo"))

async def plug(_, message):

    CatXGirl = await message.reply_text(text="Hello I am CatXGirl Bot. Im  Powerfull And Fast Telegram Bot.. [Cat X Girl](https://github.com/RishBropromax/Cat-X-Girl-Bot) "  

 

    )

    ImRishmika = """

I'm a group management bot with some useful features.

@CatXGirl_Bot

    """

    await CatXGirl.edit_text(ImRishmika)

__MODULE__ = "test"

__HELP__ = """  

#Repo - Github Repo

"""
