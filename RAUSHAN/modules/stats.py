from pyrogram import filters
from pyrogram.types import Message
import random
import asyncio
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import traceback
from pyrogram.types import Message
from pyrogram import *
from pyrogram.types import *
from config import OWNER_ID
from RAUSHAN import dev, OWNER
from RAUSHAN.database.chats import get_served_chats
from RAUSHAN.database.users import get_served_users


@dev.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(cli: dev, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_text(
        f"""آمار کلی {(await cli.get_me()).mention} :

➻ **گروه‌ها:** {chats}
➻ **کاربران:** {users}"""
    )

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : غیرفعال شده\n"
    except UserIsBlocked:
        return 400, f"{user_id} : ربات را مسدود کرده\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : شناسه کاربری نامعتبر\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@dev.on_message(filters.command("gcast") & filters.user(OWNER_ID))
async def broadcast(_, message):
    if not message.reply_to_message:
        await message.reply_text("برای پخش پیام، روی یک پیام ریپلای کنید.")
        return    
    exmsg = await message.reply_text("پخش پیام آغاز شد!")
    all_chats = (await get_served_chats()) or {}
    all_users = (await get_served_users()) or {}
    done_chats = 0
    done_users = 0
    failed_chats = 0
    failed_users = 0
    for chat in all_chats:
        try:
            await send_msg(chat, message.reply_to_message)
            done_chats += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_chats += 1

    for user in all_users:
        try:
            await send_msg(user, message.reply_to_message)
            done_users += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_users += 1
    if failed_users == 0 and failed_chats == 0:
        await exmsg.edit_text(
            f"**پخش پیام با موفقیت انجام شد ✅**\n\n**پیام به** `{done_chats}` **گروه و** `{done_users}` **کاربر ارسال شد**",
        )
    else:
        await exmsg.edit_text(
            f"**پخش پیام با موفقیت انجام شد ✅**\n\n**پیام به** `{done_chats}` **گروه و** `{done_users}` **کاربر ارسال شد**\n\n**توجه:** `به دلیل برخی مشکلات، امکان ارسال به` `{failed_users}` **کاربر و** `{failed_chats}` **گروه وجود نداشت**",
        )

@dev.on_message(filters.command("promo") & filters.user(OWNER_ID))
async def announced(_, message):
    if message.reply_to_message:
      to_send=message.reply_to_message.id
    if not message.reply_to_message:
      return await message.reply_text("برای پخش پیام، روی یک پست ریپلای کنید")
    chats = await get_served_chats() or []
    users = await get_served_users() or []
    print(chats)
    print(users)
    failed = 0
    for chat in chats:
      try:
        await dev.forward_messages(chat_id=int(chat), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception:
        failed += 1
    
    failed_user = 0
    for user in users:
      try:
        await dev.forward_messages(chat_id=int(user), from_chat_id=message.chat.id, message_ids=to_send)
        await asyncio.sleep(1)
      except Exception as e:
        failed_user += 1

    await message.reply_text("پخش پیام کامل شد. {} گروه به دلیل اخراج ربات نتوانستند پیام را دریافت کنند. {} کاربر به دلیل مسدود کردن ربات نتوانستند پیام را دریافت کنند.".format(failed, failed_user))

# کانال: @atrinmusic_tm
# مالک: @beblnn
