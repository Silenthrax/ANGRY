import random
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import LOGGER_ID as LOG_GROUP_ID
from SONALI import app 
from pyrogram.errors import RPCError
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, aiohttp
from pathlib import Path
from pyrogram.enums import ParseMode

photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]

@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):
    import random
    chat = message.chat
    link = None
    # Check if bot is admin before exporting invite link
    try:
        bot_member = await app.get_chat_member(chat.id, (await app.get_me()).id)
        is_admin = bot_member.status in ("administrator", "creator")
    except Exception:
        is_admin = False
    if is_admin:
        try:
            link = await app.export_chat_invite_link(chat.id)
            link_url = link.invite_link if hasattr(link, "invite_link") else str(link)
        except Exception:
            link = None
            link_url = None
    else:
        link_url = None
    for member in message.new_chat_members:
        if member.id == app.id:
            try:
                count = await app.get_chat_members_count(chat.id)
            except Exception:
                count = "?"
            msg = (
                f"📝 ᴍᴜsɪᴄ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ\n\n"
                f"____________________________________\n\n"
                f"📌 ᴄʜᴀᴛ ɴᴀᴍᴇ: {chat.title}\n"
                f"🍂 ᴄʜᴀᴛ ɪᴅ: {chat.id}\n"
                f"🔐 ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ: @{chat.username if chat.username else 'N/A'}\n"
                f"🛰 ᴄʜᴀᴛ ʟɪɴᴋ: {'[ᴄʟɪᴄᴋ](' + link_url + ')' if link_url else 'N/A'}\n"
                f"📈 ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs: {count}\n"
                f"🤔 ᴀᴅᴅᴇᴅ ʙʏ: {message.from_user.mention if message.from_user else 'N/A'}"
            )
            try:
                reply_markup = None
                if link_url:
                    reply_markup = InlineKeyboardMarkup([
                        [InlineKeyboardButton("sᴇᴇ ɢʀᴏᴜᴘ👀", url=link_url)]
                    ])
                if reply_markup:
                    await app.send_photo(
                        LOG_GROUP_ID,
                        photo=random.choice(photo),
                        caption=msg,
                        reply_markup=reply_markup,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                else:
                    await app.send_photo(
                        LOG_GROUP_ID,
                        photo=random.choice(photo),
                        caption=msg,
                        parse_mode=ParseMode.MARKDOWN,
                    )
            except Exception:
                # Fallback to sending text if photo or markup fails
                try:
                    await app.send_message(LOG_GROUP_ID, msg)
                except Exception:
                    pass

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id
        left = f"✫ <b><u>#𝐋ᴇғᴛ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ : {title}\n\n𝐂ʜᴀᴛ 𝐈ᴅ : {chat_id}\n\n𝐑ᴇᴍᴏᴠᴇᴅ 𝐁ʏ : {remove_by}\n\n𝐁ᴏᴛ : @{app.username}"
        await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)
        
