from CatXGirl import app

from CatXGirl.cat.commands import *

@app.on_message(command("/cmds"))

async def plug(_, message):

    CatXGirl = await message.reply_text(text="Wellcome  My  New Commands Are Coming Wait Some Time. "  

 

    )

    ImRishmika = """

I'm a group management bot with some useful features.

@CatXGirl_Bot

    """

    await CatXGirl.edit_text(ImRishmika)

__MODULE__ = "Cmds"

__HELP__ = """  

/cmds   -  My  Cmd Massege

"""
