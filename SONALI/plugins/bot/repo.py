from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI import app
from config import BOT_USERNAME
from SONALI.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
✰ 𝗪ᴇʟᴄᴏᴍᴇ ᴛᴏ 𝗧ᴇᴀᴍ 𝗦𝗜𝗟𝗘𝗡𝗧𝗛𝗥𝗔𝗫 𝗡𝗘𝗧𝗪𝗢𝗥𝗞 ꪜ 
 
✰ 𝗥ᴇᴘᴏ ᴛᴏ 𝗡ʜɪ 𝗠ɪʟᴇɢᴀ 𝗬ʜᴀ
 
✰ 𝗣ᴀʜʟᴇ 𝗣ᴀᴘᴀ 𝗕ᴏʟ 𝗥ᴇᴘᴏ 𝗢ᴡɴᴇʀ ᴋᴏ 

✰ || @silenthrax ||
 
✰ 𝗥ᴜɴ 24x7 𝗟ᴀɢ 𝗙ʀᴇᴇ 𝗪ɪᴛʜᴏᴜᴛ 𝗦ᴛᴏᴘ
 
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("𝗔ᴅᴅ ᴍᴇ 𝗠ᴀʙʏ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("𝗛ᴇʟᴘ", url="https://t.me/silenthrex"),
          InlineKeyboardButton("𝗦𝗜𝗟𝗘𝗡𝗧𝗛𝗥𝗔𝗫 ", url="https://t.me/silenthrax"),
          ],
               [
                InlineKeyboardButton("𝗦𝗜𝗟𝗘𝗡𝗧𝗛𝗥𝗔𝗫 𝗡𝗘𝗧𝗪𝗢𝗥𝗞 ꪜ", url=f"https://t.me/silenthrex"),
],
[
InlineKeyboardButton("𝗠ᴀɪɴ 𝗕ᴏᴛ", url=f"https://t.me/ANGRY_BIRD_ROBOT"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://files.catbox.moe/03na15.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
