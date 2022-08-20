from CatXGirl import app

from CatXGirl.cat.commands import *

@app.on_message(command("/Alive"))

async def plug(_, message):

    CatXGirl = await message.reply_text(text="I m Alive Bro. My New Filters Updated.. Join [CatXGirlNews](t.me/CatXGirlNews)"  

 

    )

    ImRishmika = """

I'm a group management bot with some useful features.

@CatXGirl_Bot

    """

    await CatXGirl.edit_text(ImRishmika)

__MODULE__ = "Alive"

__HELP__ = """  

/alive - alive massege

"""
