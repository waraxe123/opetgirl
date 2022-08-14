import config

from inspect import getfullargspec
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from FallenMusic import (ASSID, ASSNAME, BOT_ID, BOT_USERNAME, BOT_NAME, SUDO_USERS, app, Ass)
from FallenMusic.Helpers.Database import (approve_pmpermit, disapprove_pmpermit,
                            is_pmpermit_approved)


__MODULE__ = "Assɪsᴛᴀɴᴛ"
__HELP__ = f"""

**ɴᴏᴛᴇ :**
ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs

{config.ASS_HANDLER[0]}block [ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ] 
» ʙʟᴏᴄᴋs ᴛʜᴇ ᴜsᴇʀ ᴏɴ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.

{config.ASS_HANDLER[0]}unblock [ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ] 
» ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ ᴏɴ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.

{config.ASS_HANDLER[0]}approve [ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ] 
» ᴀᴩᴩʀᴏᴠᴇs ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ᴩᴍ ᴏɴ ʏᴏᴜʀ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.

{config.ASS_HANDLER[0]}disapprove [ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ] 
» ᴅɪsᴀᴩᴩʀᴏᴠᴇs ᴛʜᴇ ᴜsᴇʀ ᴛᴏ ᴩᴍ ᴏɴ ʏᴏᴜʀ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.

{config.ASS_HANDLER[0]}pfp [ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴩʜᴏᴛᴏ] 
» ᴄʜᴀɴɢᴇs ᴛʜᴇ ᴩғᴩ ᴏғ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜᴜɴᴛ.

{config.ASS_HANDLER[0]}bio [ᴛᴇxᴛ] 
» ᴄʜᴀɴɢᴇs ᴛʜᴇ ʙɪᴏ ᴏғ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.
"""

flood = {}


@Ass.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDO_USERS)
)
async def awaiting_message(_, message):
    user_id = message.from_user.id
    if await is_pmpermit_approved(user_id):
        return
    async for m in Ass.iter_history(user_id, limit=5):
        if m.reply_markup:
            await m.delete()
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 4:
        await message.reply_text("**» sᴩᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ. ʙʟᴏᴄᴋɪɴɢ ᴛʜɪs ᴜsᴇʀ.**")
        await Ass.send_message(
            config.LOGGER_ID,
            f"**sᴩᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ**\n\n» **sᴩᴀᴍᴍᴇʀ :** {message.from_user.mention}\n» **ᴜsᴇʀ ɪᴅ:** {message.from_user.id}",
        )
        return await Ass.block_user(user_id)
    results = await Ass.get_inline_bot_results(
        BOT_ID, f"Permit_for_PM {user_id}"
    )
    await Ass.send_inline_bot_result(
        user_id,
        results.query_id,
        results.results[0].id,
        hide_via=True,
    )


@Ass.on_message(
    filters.command("approve", prefixes=config.ASS_HANDLER)
    & filters.user(SUDO_USERS)
    & ~filters.via_bot
)
async def pm_approve(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴀᴩᴩʀᴏᴠᴇ."
        )
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        return await eor(message, text="» ᴀʟʀᴇᴀᴅʏ ᴀᴩᴩʀᴏᴠᴇᴅ ᴛᴏ ᴩᴍ.")
    await approve_pmpermit(user_id)
    await eor(message, text="» ᴀᴩᴩʀᴏᴠᴇᴅ ᴛᴏ ᴩᴍ.")


@Ass.on_message(
    filters.command("disapprove", prefixes=config.ASS_HANDLER)
    & filters.user(SUDO_USERS)
    & ~filters.via_bot
)
async def pm_disapprove(_, message):
    if not message.reply_to_message:
        return await eor(
            message, text="» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴅɪsᴀᴩᴩʀᴏᴠᴇ."
        )
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await eor(message, text="» ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀᴩᴩʀᴏᴠᴇᴅ ᴛᴏ ᴩᴍ.")
        async for m in Ass.iter_history(user_id, limit=5):
            if m.reply_markup:
                try:
                    await m.delete()
                except Exception:
                    pass
        return
    await disapprove_pmpermit(user_id)
    await eor(message, text="» ᴅɪsᴀᴩᴩʀᴏᴠᴇᴅ ᴛᴏ ᴩᴍ.")

    
@Ass.on_message(
    filters.command("pfp", prefixes=config.ASS_HANDLER)
    & filters.user(SUDO_USERS)
    & ~filters.via_bot
)
async def set_pfp(_, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴩʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴀssɪsᴛᴀɴᴛ ᴩғᴩ.")
    photo = await message.reply_to_message.download()
    try: 
        await Ass.set_profile_photo(photo=photo)   
        await eor(message, text="**» sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴩғᴩ ᴏғ ᴀssɪsᴛᴀɴᴛ.**")
    except Exception as e:
        await eor(message, text=e)
    
    
@Ass.on_message(
    filters.command("bio", prefixes=config.ASS_HANDLER)
    & filters.user(SUDO_USERS)
    & ~filters.via_bot
)
async def set_bio(_, message):
    if len(message.command) == 1:
        return await eor(message , text="» ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴀssɪsᴛᴀɴᴛ ʙɪᴏ.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try: 
            await Ass.update_profile(bio=bio) 
            await eor(message , text="**» sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ʙɪᴏ ᴏғ ᴀssɪsᴛᴀɴᴛ.**")
        except Exception as e:
            await eor(message , text=e) 
    else:
        return await eor(message , text="» ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴀssɪsᴛᴀɴᴛ ʙɪᴏ.")

flood2 = {}

@app.on_callback_query(filters.regex("pmpermit"))
async def pmpermit_cq(_, cq):
    user_id = cq.from_user.id
    data, victim = (
        cq.data.split(None, 2)[1],
        cq.data.split(None, 2)[2],
    )
    if data == "approve":
        if user_id != ASSID:
            return await cq.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ ᴍʏ ʙᴀʙʏ.")
        await approve_pmpermit(int(victim))
        return await app.edit_inline_text(
            cq.inline_message_id, "» ᴀᴩᴩʀᴏᴠᴇᴅ ᴛᴏ ᴩᴍ."
        )

    elif data == "approve_me":
        await cq.answer()
        if str(user_id) in flood2:
            flood2[str(user_id)] += 1
        else:
            flood2[str(user_id)] = 1
        if flood2[str(user_id)] > 4:
            await Ass.send_message(
                user_id, f"» sᴩᴀᴍᴍɪɴɢ ᴅᴇᴛᴇᴄᴛᴇᴅ ᴏɴ {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.\n\nʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ sᴩᴀᴍᴍᴇʀ."
            )
            await Ass.send_message(
                config.LOGGER_ID,
                f"**sᴩᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ**\n\n» **sᴩᴀᴍᴍᴇʀ :** {cq.from_user.mention}\n» **ᴜsᴇʀ ɪᴅ:** {user_id}",
            )
            return await Ass.block_user(user_id)
        await Ass.send_message(
            user_id,
            f"» ᴛʜɪs ɪs {BOT_NAME} ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ.\n\nᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴛʜᴇ ᴏᴡɴᴇʀ ᴅᴏᴇsɴ'ᴛ ᴀᴩᴩʀᴏᴠᴇ ʏᴏᴜ ᴛᴏ ᴩᴍ.",
        )


async def pmpermit_func(answers, user_id, victim):
    if user_id != ASSID:
        return
    caption = f"ʜᴇʏ,\n\nᴛʜɪs ɪs {ASSNAME}, ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ {BOT_NAME}.\nᴩʟᴇᴀsᴇ ᴅᴏɴ'ᴛ sᴩᴀᴍ ᴍᴇssᴀɢᴇs ʜᴇʀᴇ (ʏᴏᴜ'ʟʟ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ɢᴇᴛ ʙʟᴏᴄᴋᴇᴅ ᴏɴ sᴇɴᴅɪɴɢ 4 ᴄᴏɴᴄᴜʀʀᴇɴᴛ ᴍᴇssᴀɢᴇs.)"
    ass_markup2 = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴀᴩᴩʀᴏᴠᴇ ᴍᴇ", callback_data=f"pmpermit approve_me a"
                ),
                InlineKeyboardButton(
                    text="ᴀᴩᴩʀᴏᴠᴇ", callback_data=f"pmpermit approve {victim}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="sᴜᴩᴩᴏʀᴛ", url=config.SUPPORT_CHAT
                )
            ],
        ]
    )
    answers.append(
        InlineQueryResultArticle(
            title="ᴛʜɪs_ɪs_ɴᴏᴛ_ғᴏʀ_ʏᴏᴜ",
            reply_markup=ass_markup2,
            input_message_content=InputTextMessageContent(caption),
        )
    )
    return answers


@app.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.split()[0] == "Permit_for_PM":
            user_id = query.from_user.id
            victim = text.split()[1]
            answerss = await pmpermit_func(answers, user_id, victim)
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=2
            )
    except:
        return


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
