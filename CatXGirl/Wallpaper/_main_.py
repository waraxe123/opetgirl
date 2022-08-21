from CatXGirl.Wallpaper import app

import pyrogram, random

from pyrogram import filters, idle

from pyrogram.errors import FloodWait

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from CatXGirl.Wallpaper.wall import get_wallpapers, get_unsplash

from CatXGirl.Wallpaper.db_funcs import *

WSTART = """

**🔮 Hello {username} Wellcome Wallpaper Menu..**

You Wan't Download HD Wallapers Use Me Send /whelp



"""

WHELP = """

**🇱🇰 How To Use Me ?**

**To Download Wallpapers -** `/wall <search>`

**To Download Wallpapers From Unsplash - ** `/unsplash <search>`

**♻️🔥 Example:** 

`/wall anime`

`/unsplash cat`

"""

# Commands

@app.on_message(filters.command("wstart"))

async def start(bot, message: Message):

  await message.reply_photo("https://telegra.ph/file/a5cda781d0f763e4a5f7f.jpg",caption=START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help 😊", callback_data="Whelp_menu"), InlineKeyboardButton(text="Repo 🇱🇰", url="https://github.com/RishbroProMax/Cat-X-Girl-Bot")]]))

@app.on_message(filters.command("whelp"))

async def help(bot, message: Message):

  await message.reply_photo("https://telegra.ph/file/a5cda781d0f763e4a5f7f.jpg",caption=HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back 🌹", callback_data="wstart_menu")]]))

@app.on_message(filters.command("wall") & filters.incoming & filters.text & ~filters.forwarded & (

  filters.group | filters.private))

async def wall(bot, message: Message):

  try:

    text = message.text.replace("wall","").replace("/","").replace("@CatXGirl_Bot,"").strip().upper()

    

    if text == "":

      return await message.reply_text(HELP)

    x = await message.reply_text("`🔍 Searching Wallpapers For You...`")  

    wall = await get_wallpapers(text)

      

    if "error" in wall:

      return await x.edit(f"`❌ Something Went Wrong...`\n\nReport This Error In @CatXGirlSupport \n\n`{wall}`")

    

    if "nonee" in wall:

      return await x.edit(f"`❌ Something Went Wrong...`\n\n`{wall}`")

    

    img = random.choice(wall)

      

    await x.edit("`🔄 Got It... Now Sending You`")

    

    id = await save_image(img)

    await message.reply_photo(img,caption="**🏞 Wallpaper By @CatXGirl_Bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Upload As File 📁", callback_data=f"wall {id}")]]))

    

    await x.delete()

  except FloodWait:

    pass

  except Exception as e:

    try:

      await x.delete()

    except:

      pass

    return await message.reply_text("`❌ Something Went Wrong...`\n\nReport This Error In @CatXGirlSupport\n\n" + str(e))

@app.on_message(filters.command("unsplash") & filters.incoming & filters.text & ~filters.forwarded & (

  filters.group | filters.private))

async def unsplash(bot, message: Message):

  try:

    text = message.text.replace("unsplash","").replace("/","").replace("@CatXGirl_Bot","").strip().upper()

    

    if text == "":

      return await message.reply_text(HELP)

    x = await message.reply_text("`🔍 Searching Wallpapers For You...`")  

    wall = await get_unsplash(text)

      

    if "error" in wall:

      return await x.edit(f"`❌ Something Went Wrong...`\n\nReport This Error In @CatXGirlSupport \n\n`{wall}`")

    

    if "nonee" in wall:

      return await x.edit(f"`❌ Something Went Wrong...`\n\n`{wall}`")

    

    wall = random.choice(wall)

      

    await x.edit("`🔄 Got It... Now Sending You`")

    id = await save_image(wall)

    

    await message.reply_photo(wall,caption="**🏞 Wallpaper By @CatXGirl_Bot**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Upload As File 📁", callback_data=f"wall {id}")]]))

    

    await x.delete()

  except FloodWait:

    pass

  except Exception as e:

    try:

      await x.delete()

    except:

      pass

    return await message.reply_text("`❌ Something Went Wrong...`\n\nReport This Error In @CatXGirlSupport ")

    

# Callbacks

@app.on_callback_query(filters.regex("wstart_menu"))

async def wstart_menu(_,query):

  await query.answer()

  await query.message.edit(START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", callback_data="Whelp_menu"),InlineKeyboardButton(text="Repo", url="https://github.com/RishbroPromax/Cat-X-Girl-Bot")]]))

@app.on_callback_query(filters.regex("whelp_menu"))

async def whelp_menu(_,query):

  await query.answer()

  await query.message.edit(HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="wstart_menu")]]))

@app.on_callback_query(filters.regex("wall"))

async def logo_doc(_,query):

  await query.answer()

  try:

    x = await query.message.reply_text("`🔄 Sending You The Wallpaper As File`")

    await query.message.edit_reply_markup(reply_markup=None)

    id = query.data.replace("wall","").strip()

    link = await get_image(id)

    await query.message.reply_document(link,caption="**🏞 Wallpaper By @CatXGirl_Bot**")

    await del_image(id)

  except FloodWait:

    pass

  except Exception as e:

    try:

      return await x.edit(f"`❌ Something Went Wrong...`\n\nReport This Error In @CatXGirlSupport \n\n`{str(e)}`")

    except:

      return

    

  return await x.delete()

if __name__ == "__main__":

  print("==================================")

  print("[INFO]: Cat X Girl Logo Filter Is Fine")

  print("==========JOIN @CatXGirlSupport =========")

  idle()

  print("[INFO]: Logo Fillter Stoped")
