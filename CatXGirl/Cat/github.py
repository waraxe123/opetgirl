from CatXGirl import app

from CatXGirl.cat.commands import *

@app.on_message(command("Github"))

async def plug(_, message):

    CatXGirl = await message.reply_text(text="Hello I am CatXGirl Bot. [Click Here](https://github.com/RishBropromax/Cat-X-Girl-Bot) Visite My Repository. 🇱🇰🔥 "  

 
    )

    ImRishmika = """

I'm a group management bot with some useful features.

@CatXGirl_Bot

    """

    await CatXGirl.edit_text(ImRishmika)

__MODULE__ = "test"

__HELP__ = """  

/Github - Github Repo

"""
