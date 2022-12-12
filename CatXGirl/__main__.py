import importlib
import re
import time
from platform import python_version as y
from sys import argv
from typing import Optional

from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import FallenRobot.modules.sql.users_sql as sql
from FallenRobot import (
    BOT_NAME,
    BOT_USERNAME,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from FallenRobot.modules import ALL_MODULES
from FallenRobot.modules.helper_funcs.chat_status import is_user_admin
from FallenRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
*ʜᴇʏ* {}, 🤡

*✬ ᴛʜɪs ɪs* {} !
*ʙᴏᴛ ᴍᴀɴᴀᴊᴇᴍᴇɴ ɢʀᴜᴘ ᴛᴇʟᴇɢʀᴀᴍ ʏᴀɴɢ ᴋᴜᴀᴛ ᴅᴇɴɢᴀɴ ʙᴇʙᴇʀᴀᴘᴀ ꜰɪᴛᴜʀ ʏᴀɴɢ ᴍᴇɴɢᴀɢᴜᴍᴋᴀɴ ᴅᴀɴ ʙᴇʀɢᴜɴᴀ.*
──────────────────
*✬ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ɪɴꜰᴏʀᴍᴀsɪ ᴛᴇɴᴛᴀɴɢ ᴍᴏᴅᴜʟ ᴅᴀɴ ᴘᴇʀɪɴᴛᴀʜ.*
"""


buttons = [
    [
        InlineKeyboardButton(
            text="🧑‍🔧 ᴀᴅᴅ ᴍᴇ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    
    
        InlineKeyboardButton(text="❓ᴄᴏᴍᴍᴀɴᴅs", callback_data="gusion_"),
    ],
    [
        InlineKeyboardButton(text="💰 ᴅᴏɴᴀᴛᴇ", callback_data="fallen_"),
        InlineKeyboardButton(text="🏆 sᴜᴩᴩᴏʀᴛ", callback_data="sayang_"),
    ],
    [
        InlineKeyboardButton(text="👑 ᴏᴡɴᴇʀ", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="📯 sᴏᴜʀᴄᴇ", callback_data="source_"),
    ],
]

HELP_STRINGS = f"""
*» {BOT_NAME} ᴇxᴄʟᴜsɪᴠᴇ ꜰᴇᴀᴛᴜʀᴇs*

➲ /start : ꜱᴛᴀʀᴛꜱ ᴍᴇ | ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴅᴏɴᴇ ɪᴛ​.
➲ /donate : sᴜᴘᴘᴏʀᴛ ᴍᴇ ʙʏ ᴅᴏɴᴀᴛɪɴɢ ꜰᴏʀ ᴍʏ ʜᴀʀᴅᴡᴏʀᴋ​.
➲ /help  : ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ꜱᴇᴄᴛɪᴏɴ.
  ‣ ɪɴ ᴘᴍ : ᴡɪʟʟ ꜱᴇɴᴅ ʏᴏᴜ ʜᴇʟᴘ​ ꜰᴏʀ ᴀʟʟ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇꜱ.
  ‣ ɪɴ ɢʀᴏᴜᴘ : ᴡɪʟʟ ʀᴇᴅɪʀᴇᴄᴛ ʏᴏᴜ ᴛᴏ ᴘᴍ, ᴡɪᴛʜ ᴀʟʟ ᴛʜᴀᴛ ʜᴇʟᴘ​ ᴍᴏᴅᴜʟᴇꜱ."""

DONATE_STRING = """ʜᴇʏ ʙᴀʙʏ,
  sᴇɴᴀɴɢ ᴍᴇɴᴅᴇɴɢᴀʀ ʙᴀʜᴡᴀ ᴀɴᴅᴀ ɪɴɢɪɴ ᴍᴇɴʏᴜᴍʙᴀɴɢ.

🍩🍩🍩🍩🍩🍩."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("FallenRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_sticker(
                "CAACAgUAAx0CW7OmbAACMS1jdqAAAaYgfBjpYwbv3uN02k5evskAAoUFAAKANqlUrinPET4g6CwrBA"
            )
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass


@run_async 
def Mati_muta_callback(update: Update, context: CallbackContext): 
    query = update.callback_query 
    if query.data == "mati_": 
       uptime = get_readable_time((time.time() - StartTime)) 
       query.message.edit_text( 
           text=f"*🥀 sᴜᴅᴏᴇʀs ᴀɴᴅ ᴏᴡɴᴇʀ ᴄᴏᴍᴍᴀɴᴅs :*" 
           "\n\n🥺 ᴀᴅᴅ & ʀᴇᴍᴏᴠᴇ sᴜᴅᴏᴇʀs :"
           "\n\n/addsudo [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ]"
           "\n/delsudo [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ.]"
           "\n\n🥶 ʜᴇʀᴏᴋᴜ :"
           "\n\n/usage : sʜᴏᴡs ᴛʜᴇ ᴅʏɴᴏ ᴜsᴀɢᴇ ᴏғ ᴛʜᴇ ᴍᴏɴᴛʜ."
           "\n\n🤯 ᴄᴏɴғɪɢ ᴠᴀʀɪᴀʙʟᴇs:"
           "\n\n/get_var : ɢᴇᴛ ᴀ ᴄᴏɴғɪɢ ᴠᴀʀ ғʀᴏᴍ ʜᴇʀᴏᴋᴜ ᴏʀ .ᴇɴᴠ."
           "\n/del_var : ᴅᴇʟᴇᴛᴇ ᴀ ᴄᴏɴғɪɢ ᴠᴀʀ ᴏɴ ʜᴇʀᴏᴋᴜ ᴏʀ .ᴇɴᴠ."
           "\n/set_var [ᴠᴀʀ ɴᴀᴍᴇ] [ᴠᴀʟᴜᴇ] : sᴇᴛ ᴏʀ ᴜᴩᴅᴀᴛᴇ ᴀ ᴄᴏɴғɪɢ ᴠᴀʀ ᴏɴ ʜᴇʀᴏᴋᴜ ᴏʀ .ᴇɴᴠ."
           "\n\n🤓 ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs:"
           "\n\n/restart : ʀᴇsᴛᴀʀᴛs ʏᴏᴜʀ ʙᴏᴛ."
           "\n\n/update : ᴜᴩᴅᴀᴛᴇs ᴛʜᴇ ʙᴏᴛ ғʀᴏᴍ ᴛʜᴇ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ."
           "\n\n/speedtest : ᴄʜᴇᴄᴋ ʙᴏᴛ's sᴇʀᴠᴇʀ sᴩᴇᴇᴅ."
           "\n\n/maintenance [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴏғ ʏᴏᴜʀ ʙᴏᴛ."
           "\n\n/logger [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ʙᴏᴛ ᴡɪʟʟ sᴛᴀʀᴛ ʟᴏɢɢɪɴɢ ᴛʜᴇ ᴀᴄᴛɪᴠɪᴛɪᴇs ʜᴀᴩᴩᴇɴ ᴏɴ ʙᴏᴛ."
           "\n\n/get_log [ɴᴜᴍʙᴇʀ ᴏғ ʟɪɴᴇs] : ɢᴇᴛ ʟᴏɢs ᴏғ ʏᴏᴜʀ ʙᴏᴛ [ᴅᴇғᴀᴜʟᴛ ᴠᴀʟᴜᴇ ɪs 100 ʟɪɴᴇs]"
           "\n\n💔 ғᴏʀ ᴩʀɪᴠᴀᴛᴇ ʙᴏᴛ ᴏɴʟʏ :"
           "\n\n/authorize [ᴄʜᴀᴛ ɪᴅ] : ᴀʟʟᴏᴡs ᴀ ᴄʜᴀᴛ ғᴏʀ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ."
           "\n/unauthorize [ᴄʜᴀᴛ ɪᴅ] : ᴅɪsᴀʟʟᴏᴡs ᴛʜᴇ ᴀʟʟᴏᴡᴇᴅ ᴄʜᴀᴛ."
           "\n/authorized : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀʟʟᴏᴡᴇᴅ ᴄʜᴀᴛs.",
           parse_mode=ParseMode.MARKDOWN, 
           disable_web_page_preview=True, 
           reply_markup=InlineKeyboardMarkup( 
               [
                   [
                       InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"), 
                   ],
               ]
           ),
       )
        
        
@run_async 
def Berak_borak_callback(update: Update, context: CallbackContext):
    query = update.callback_query 
    if query.data == "berak_":  
       uptime = get_readable_time((time.time() - StartTime)) 
       query.message.edit_text( 
           text=f"*😅ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴡɪᴛʜ ʙᴏᴛ.*" 
           "\n\n/start : sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ."
           "\n\n/help : ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs."
           "\n\n/reboot : ʀᴇʙᴏᴏᴛs ᴛʜᴇ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ."
           "\n\n/settings : sʜᴏᴡs ᴛʜᴇ ɢʀᴏᴜᴩ sᴇᴛᴛɪɴɢs ᴡɪᴛʜ ᴀɴ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ɪɴʟɪɴᴇ ᴍᴇɴᴜ."
           "\n\n/sudolist : sʜᴏᴡs ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀs ᴏғ ᴍᴜsɪᴄ ʙᴏᴛ.",
           parse_mode=ParseMode.MARKDOWN, 
           disable_web_page_preview=True, 
           reply_markup=InlineKeyboardMarkup( 
               [
                   [
                       InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"), 
                   ]
               ]
           ),
       )
        
        
@run_async
def Rangu_rungi_callback(update: Update, context: CallbackContext): 
    query = update.callback_query 
    if query.data == "rangu_": 
       uptime = get_readable_time((time.time() - StartTime)) 
       query.message.edit_text( 
           text=f"*🤑 ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs :*" 
           "\n\n/activevoice : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ᴏɴ ᴛʜᴇ ʙᴏᴛ."
           "\n/activevideo : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ."
           "\n/autoend [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ sᴛʀᴇᴀᴍ ᴀᴜᴛᴏ ᴇɴᴅ ɪғ ɴᴏ ᴏɴᴇ ɪs ʟɪsᴛᴇɴɪɴɢ.",


           parse_mode=ParseMode.MARKDOWN, 
           disable_web_page_preview=True, 
           reply_markup=InlineKeyboardMarkup( 
               [
                   [
                       InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                   ],
               ]
           ),
       )
        
        
@run_async
def Kacang_kucang_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "kacang_":
       uptime = get_readable_time((time.time() - StartTime))
       query.message.edit_text(
           text=f"*🤨 sᴇʀᴠᴇʀ ᴩʟᴀʏʟɪsᴛs :*"
           "\n\n/playlist : ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀs."
           "\n\n/deleteplaylist : ᴅᴇʟᴇᴛᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʀᴀᴄᴋ ɪɴ ʏᴏᴜʀ ᴩʟᴀʏʟɪsᴛ."
           "\n\n/play : sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ғʀᴏᴍ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀ.",
           parse_mode=ParseMode.MARKDOWN,
           disable_web_page_preview=True, 
           reply_markup=InlineKeyboardMarkup( 
               [
                   [
                       InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                   ],
               ]
           ),
       )
        
        
@run_async
def Tapai_topai_callback(update: Update, context: CallbackContext): 
    query = update.callback_query
    if query.data == "tapai_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*💞 ᴩʟᴀʏ ᴄᴏᴍᴍᴀɴᴅs:.*"
            "\n\nc sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ."
            "\nv sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ."
            "\nforce sᴛᴀɴᴅs ғᴏʀ ғᴏʀᴄᴇ ᴩʟᴀʏ."
            "\n\n/play ᴏʀ /vplay ᴏʀ /cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ."
            "\n\n/playforce ᴏʀ /vplayforce ᴏʀ /cplayforce : ғᴏʀᴄᴇ ᴩʟᴀʏ sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ."
            "\n\n/channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                    ],
                ]
            ),
        )
        
        
@run_async
def Kecoa_kacoa_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "kecoa_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*🍑 ᴩɪɴɢ ᴄᴏᴍᴍᴀɴᴅ :.*" 
            "\n\n/ping : sʜᴏᴡ ᴛʜᴇ ᴩɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ."
            "\n\n/stats : ɢᴇᴛ ᴛᴏᴩ 10 ᴛʀᴀᴄᴋ ɢʟᴏʙᴀʟ sᴛᴀᴛs, ᴛᴏᴩ 10 ᴜsᴇʀs ᴏғ ᴛʜᴇ ʙᴏᴛ, ᴛᴏᴩ 10 ᴄʜᴀᴛs ᴏɴ ᴛʜᴇ ʙᴏᴛ, ᴛᴏᴩ 10 ᴩʟᴀʏᴇᴅ ɪɴ ᴛʜᴇ ᴄʜᴀᴛ ᴀɴᴅ ᴍᴀɴʏ ᴍᴏʀᴇ..",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup( 
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                    ],
                ]
            ),
        )
        
        
@run_async
def Manuk_munak_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "manuk_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*😉 ᴇxᴛʀᴀs :.*"
            "\n\n/loop [ᴅɪsᴀʙʟᴇ/ᴇɴᴀʙʟᴇ] ᴏʀ [ʙᴇᴛᴡᴇᴇɴ 1:10]"
            "\n: ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙᴏᴛ ᴡɪʟʟ ᴩʟᴀʏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴩ ғᴏʀ 10 ᴛɪᴍᴇs ᴏʀ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏᴏᴩs."
            "\n\n/shuffle : sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs."
            "\n\n/seek : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ."
            "\n\n/seekback : ʙᴀᴄᴋᴡᴀʀᴅ sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ."
            "\n\n/lyrics [sᴏɴɢ ɴᴀᴍᴇ] : sᴇᴀʀᴄʜ ʟʏʀɪᴄs ғᴏʀ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ ᴀɴᴅ sᴇɴᴅ ᴛʜᴇ ʀᴇsᴜʟᴛs.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                    ],
                ]
            ),
        )
        
        
@run_async
def Babi_boba_callback(update: Update, context: CallbackContext): 
    query = update.callback_query
    if query.data == "babi_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*🤬 ɢʙᴀɴ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :.*" 
            "\n\n/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ."
            "\n\n/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ."
            "\n\n/gbannedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇʀ ᴜsᴇʀs.",
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                    ],
                ]
            ),
        )
        
        
@run_async   
def Gagah_tidak_callback(update: Update, context: CallbackContext): 
    query = update.callback_query
    if query.data == "gagah_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text( 
            text=f"*🍒 ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs] :.*"
            "\n\n/broadcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ."
            "\n\nʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs:"
            "\n-pin : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs."
            "\n-pinloud : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ sᴇɴᴅ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴇᴍʙᴇʀs."
            "\n-user : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ."
            "\n-assistant : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ."
            "\n-nobot : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ."
            "\n\n**ᴇxᴀᴍᴩʟᴇ:** `/broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ`.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                    ],
                ]
            ),
        )
        
            
@run_async
def Makan_nasi_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "makan_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*😒 ʙʟᴀᴄᴋʟɪsᴛ ᴄʜᴀᴛ :*"
            "\nʙʟᴀᴄᴋʟɪsᴛ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]."
            "\n\n/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ."
            "\n\n/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ."
            "\n\n/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs."
            "\n\n\n😤 ʙʟᴏᴄᴋ ᴜsᴇʀs:."
            "\n\n/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ] : sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ, sᴏ ᴛʜᴀᴛ ʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs."
            "\n\n/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ."
            "\n\n/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs.",
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup( 
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"),
                    ],
                ]
            ),
        )
        
        
@run_async
def Minum_gelas_callback(update: Update, context: CallbackContext): 
    query = update.callback_query
    if query.data == "minum_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*😜 ᴀᴜᴛʜ ᴜsᴇʀs :*"
            "\nᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ. [ᴀᴅᴍɪɴs ᴏɴʟʏ]."
            "\n\n/auth [ᴜsᴇʀɴᴀᴍᴇ] : ᴀᴅᴅ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ."
            "\n\n/unauth [ᴜsᴇʀɴᴀᴍᴇ] : ʀᴇᴍᴏᴠᴇ ᴀ ᴀᴜᴛʜ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ."
            "\n\n/authusers : sʜᴏᴡs ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴩ.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"), 
                    ],
                ]
            ),
        )
        
        
@run_async
def Jurig_atah_callback(update: Update, context: CallbackContext):
    query = update.callback_query 
    if query.data == "jurig_": 
        uptime = get_readable_time((time.time() - StartTime)) 
        query.message.edit_text( 
            text=f"*🙄 ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:*" 
            "\n\n*nᴊᴜsᴛ ᴀᴅᴅ ᴄ ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.*"
            "\n\n/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ."
            "\n\n/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ."
            "\n\n/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ."
            "\n\n/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ."
            "\n\n/player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ."
            "\n\n/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ.",
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup(
                [ 
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="harlay_"), 
                    ],
                ]
            ),
        )
        
                    
@run_async
def Harlay_sulap_callback(update: Update, context: CallbackContext): 
    query = update.callback_query
    if query.data == "harlay_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*💽 ʙᴀɴᴛᴜᴀɴ ᴘᴇʀɪɴᴛᴀʜ ᴍᴜsɪᴄ.*"
            "\n\n*ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ɪɴꜰᴏʀᴍᴀsɪ ʟᴇʙɪʜ ʟᴀɴᴊᴜᴛ. ᴊɪᴋᴀ ᴀɴᴅᴀ ᴍᴇɴɢʜᴀᴅᴀᴘɪ ᴍᴀsᴀʟᴀʜ ᴅᴀʟᴀᴍ ᴘᴇʀɪɴᴛᴀʜ, ᴀɴᴅᴀ ᴅᴀᴘᴀᴛ ᴍᴇɴɢʜᴜʙᴜɴɢɪ ᴘᴇᴍɪʟɪᴋ ʙᴏᴛ sᴀʏᴀ ᴀᴛᴀᴜ ʙᴇʀᴛᴀɴʏᴀ ᴅᴀʟᴀᴍ ᴏʙʀᴏʟᴀɴ ᴅᴜᴋᴜɴɢᴀɴ.*"
            "\n\n*sᴇᴍᴜᴀ ᴘᴇʀɪɴᴛᴀʜ ᴅᴀᴘᴀᴛ ᴅɪɢᴜɴᴀᴋᴀɴ ᴅᴇɴɢᴀɴ: /*",
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴀᴅᴍɪɴ", callback_data="jurig_"
                        ),
                        InlineKeyboardButton(
                            text="ᴀᴜᴛʜ", callback_data="minum_"
                        ),
                    
                        InlineKeyboardButton(
                            text="ʙʟᴀᴄᴋʟɪsᴛ", callback_data="makan_"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="gagah_"
                        ),
                        InlineKeyboardButton(
                            text="ɢʙᴀɴ", callback_data="babi_"
                        ),
                        InlineKeyboardButton(
                            text="ʟʏʀɪᴄs", callback_data="manuk_"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴘɪɴɢ", callback_data="kecoa_"
                        ),
                        InlineKeyboardButton(
                            text="ᴘʟᴀʏ", callback_data="tapai_"
                        ),
                        InlineKeyboardButton(
                            text="ᴘʟᴀʏʟɪsᴛ", callback_data="kacang_"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴠɪᴅᴇᴏᴄʜᴀᴛs", callback_data="rangu_"
                        ),
                        InlineKeyboardButton(
                            text="sᴛᴀʀᴛ", callback_data="berak_"
                        ),
                        InlineKeyboardButton(
                            text="sᴜᴅᴏ", callback_data="mati_"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="gusion_"), 
                    ],
                ]
            ),
        )
                        
                        
@run_async
def Gusion_lancelot_callback(update: Update, context: CallbackContext):  
    query = update.callback_query 
    if query.data == "gusion_": 
        uptime = get_readable_time((time.time() - StartTime)) 
        query.message.edit_text( 
            text=f"*🛠️ ʙᴀɴᴛᴜᴀɴ ᴘᴇʀɪɴᴛᴀʜ*" 
            "\n\n*ᴘɪʟɪʜ ᴛᴏᴍʙᴏʟ ᴅɪʙᴀᴡᴀʜ ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ʙᴀɴᴛᴜᴀɴ ᴘᴇʀɪɴᴛᴀʜ..*",  
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup( 
                [ 
                    [ 
                        InlineKeyboardButton( 
                            text="⚙️ ᴍᴀɴᴀɢᴇ", callback_data="help_back"
                        ),
                        InlineKeyboardButton(
                            text="🎼 ᴍᴜsɪᴋ", callback_data="harlay_" 
                        ), 
                    ], 
                    [ 
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="fallen_back"), 
                    ],
                ]
            ),
        )
    
    
@run_async
def Sayang_kamu_callback(update: Update, context: CallbackContext): 
    query = update.callback_query
    if query.data == "sayang_": 
        uptime = get_readable_time((time.time() - StartTime)) 
        query.message.edit_text( 
            text=f"*🐧 ʙᴀɴᴛᴜᴀɴ ᴘᴇʀɪɴᴛᴀʜ ᴅᴇᴀᴋ*" 
            "\n\n*ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ʙᴀɴᴛᴜᴀɴ ᴘᴇʀɪɴᴛᴀʜ ᴅᴇᴀᴋ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ.*", 
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup( 
                [ 
                    [ 
                        InlineKeyboardButton(
                            text="ᴀᴜᴛᴏᴅᴇᴀᴋ", url="http://my.telegram.org/delete" 
                        ),
                        InlineKeyboardButton( 
                            text="ᴀᴜᴛᴏᴋᴏɪᴛ", url="https://t.me/https://t.me/c/1715488319/220857"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="fallen_back"), 
                    ],
                ]
            ),
        )
        
        
@run_async
def Fallen_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "fallen_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*ʜᴇʏ,*👋\n  *ᴛʜɪs ɪs {BOT_NAME}*"
            "\n*ᴀ ʙᴏᴛ ᴍᴀɴᴀᴊᴇᴍᴇɴ ɢʀᴜᴘ ʏᴀɴɢ ᴋᴜᴀᴛ ᴅɪʙᴜᴀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀɴᴛᴜ ᴀɴᴅᴀ ᴍᴇɴɢᴇʟᴏʟᴀ ɢʀᴜᴘ ᴀɴᴅᴀ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ ᴅᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʟɪɴᴅᴜɴɢɪ ɢʀᴜᴘ ᴀɴᴅᴀ ᴅᴀʀɪ sᴄᴀᴍᴍᴇʀ ᴅᴀɴ sᴘᴀᴍᴍᴇʀ.*"
            "\n*ᴅɪᴛᴜʟɪs ᴅɪ ᴘʏᴛʜᴏɴ ᴅᴇɴɢᴀɴ sǫʟᴀʟᴄʜᴇᴍʏ ᴅᴀɴ ᴍᴏɴɢᴏᴅʙ sᴇʙᴀɢᴀɪ ᴅᴀᴛᴀʙᴀsᴇ.*"
            "\n\n────────────────────"
            f"\n*➻ ᴜᴩᴛɪᴍᴇ »* {uptime}"
            f"\n*➻ ᴜsᴇʀs »* {sql.num_users()}"
            f"\n*➻ ᴄʜᴀᴛs »* {sql.num_chats()}"
            "\n────────────────────"
            "\n\n*• ᴊɪᴋᴀ ᴋᴀʟɪᴀɴ ᴍᴇɴʏᴜᴋᴀɪ ᴛᴏᴅᴏ ᴅᴀɴ ɪɴɢɪɴ ʙᴇʀᴅᴏɴᴀsɪ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀɴᴛᴜ ᴀɢᴀʀ ᴛᴏᴅᴏ ᴛᴇᴛᴀᴘ ᴀᴋᴛɪғ ᴛᴇʀᴜs.*"
            "\n\n*• ᴋᴀʟɪᴀɴ ʙɪsᴀ ʙᴇʀᴅᴏɴᴀsɪ ᴅᴇɴɢᴀɴ ᴠɪᴀ ᴏᴠᴏ 087845681216 ᴀᴛᴀᴜ ᴋᴀʟɪᴀɴ ʙɪsᴀ ʜᴜʙᴜɴɢɪ ᴏᴡɴᴇʀ ᴅɪʙᴀᴡᴀʜ ɪɴɪ.*"
            "\n\n*• ᴅᴀɴ ᴜɴᴛᴜᴋ ʏᴀɴɢ sᴜᴅᴀʜ ʙᴇʀᴅᴏɴᴀsɪ sᴀʏᴀ ᴜᴄᴀᴘᴋᴀɴ ᴛᴇʀɪᴍᴀᴋᴀsɪʜ ʙᴀɴʏᴀᴋ 🙏.*"
            f"\n\n➻ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ʏᴀɴɢ ᴅɪʙᴇʀɪᴋᴀɴ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ʙᴀɴᴛᴜᴀɴ ᴅᴀɴ ɪɴꜰᴏʀᴍᴀsɪ ʟᴇʙɪʜ ʟᴀɴᴊᴜᴛ ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ {BOT_NAME}.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴜᴩᴩᴏʀᴛ", url="https://t.me/gabutmaximall"
                        ),
                        InlineKeyboardButton(
                            text="ᴄʜᴀɴɴᴇʟ", url="https://t.me/yahkenatipu"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴅᴇᴠᴇʟᴏᴩᴇʀ", url="https://t.me/ItsProf"
                        ),
                        InlineKeyboardButton(
                            text="ᴍᴀɪɴᴛᴀɪɴᴇʀ",
                            url="https://t.me/todoshotou"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="fallen_back"),
                    ],
                ]
            ),
        )
    
    elif query.data == "fallen_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


@run_async
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=f"""
*ʜᴇʏ,
 ᴛʜɪs ɪs {BOT_NAME},
ʀᴇᴘᴏ ɪɴɪ ᴅɪ ᴊᴜᴀʟ ʙᴀʀᴀɴɢ ᴋᴀʟɪ ᴀᴅᴀ ʏᴀɴɢ ᴍɪɴᴀᴛ.*
ʜᴜʙᴜɴɢɪ » [ItsProf](https://t.me/ItsProf).





""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="source_back")]]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʜᴇʟᴘ​",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴏᴩᴇɴ ʜᴇʀᴇ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs​",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != 1356469075 and DONATION_LINK:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {BOT_NAME} sᴏʀᴄᴇ ᴄᴏᴅᴇ ɪs [todo](https://t.me/ItsProf)."
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                photo=START_IMG,
                caption=f"""
ㅤ🥀 {BOT_NAME} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ...

┏•❅────✧❅✦❅✧────❅•┓
ㅤ★ **ᴘʏᴛʜᴏɴ :** `{y()}`
ㅤ★ **ʟɪʙʀᴀʀʏ :** `{telever}`
ㅤ★ **ᴛᴇʟᴇᴛʜᴏɴ :** `{tlhver}`
ㅤ★ **ᴩʏʀᴏɢʀᴀᴍ :** `{pyrover}`
┗•❅────✧❅✦❅✧────❅•┛""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Fallen_about_callback, pattern=r"fallen_"
    )
    muta_callback_handler = CallbackQueryHandler(
        Mati_muta_callback, pattern=r"mati_"
    )
    borak_callback_handler = CallbackQueryHandler(
        Berak_borak_callback, pattern=r"berak_"
    )
    rungi_callback_handler = CallbackQueryHandler(
        Rangu_rungi_callback, pattern=r"rangu_" 
    )
    kucang_callback_handler = CallbackQueryHandler(
        Kacang_kucang_callback, pattern=r"kacang_"
    )
    topai_callback_handler = CallbackQueryHandler(
        Tapai_topai_callback, pattern=r"tapai_"
    )
    kacoa_callback_handler = CallbackQueryHandler(
        Kecoa_kacoa_callback, pattern=r"kecoa_"
    )
    munak_callback_handler = CallbackQueryHandler(
        Manuk_munak_callback, pattern=r"manuk_"
    )
    boba_callback_handler = CallbackQueryHandler(
        Babi_boba_callback, pattern=r"babi_" 
    )
    tidak_callback_handler = CallbackQueryHandler(
        Gagah_tidak_callback, pattern=r"gagah_"
    )
    nasi_callback_handler = CallbackQueryHandler(
        Makan_nasi_callback, pattern=r"makan_"
    )
    gelas_callback_handler = CallbackQueryHandler(
        Minum_gelas_callback, pattern=r"minum_"
    )
    atah_callback_handler = CallbackQueryHandler(
        Jurig_atah_callback, pattern=r"jurig_"
    )
    sulap_callback_handler = CallbackQueryHandler(
        Harlay_sulap_callback, pattern=r"harlay_"
    )
    lancelot_callback_handler = CallbackQueryHandler(
        Gusion_lancelot_callback, pattern=r"gusion_"
    )
    kamu_callback_handler = CallbackQueryHandler(
        Sayang_kamu_callback, pattern=r"sayang_"
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_"
    )

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(muta_callback_handler)
    dispatcher.add_handler(borak_callback_handler)
    dispatcher.add_handler(rungi_callback_handler)
    dispatcher.add_handler(kucang_callback_handler)
    dispatcher.add_handler(topai_callback_handler)
    dispatcher.add_handler(kacoa_callback_handler)
    dispatcher.add_handler(munak_callback_handler)
    dispatcher.add_handler(boba_callback_handler)
    dispatcher.add_handler(tidak_callback_handler)
    dispatcher.add_handler(nasi_callback_handler)
    dispatcher.add_handler(gelas_callback_handler)
    dispatcher.add_handler(atah_callback_handler)
    dispatcher.add_handler(sulap_callback_handler)                   
    dispatcher.add_handler(lancelot_callback_handler)
    dispatcher.add_handler(kamu_callback_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN, certificate=open(CERT_PATH, "rb"))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
