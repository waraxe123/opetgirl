from CatXGirl import app

from CatXGirl.cat.utils.commands import *

@app.on_message(command("test"))

async def plug(_, message):

    CatXGirl = await message.reply_text(text="Hello I am CatXGirl Bot"

    )

    ImRishmika = """

I'm a group management bot with some useful features.

CatXGirl_Bot

    """

    await CatXGirl.edit_text(ImRishmika)

__MODULE__ = "test"

__HELP__ = """  

/test - test cmd here

"""
