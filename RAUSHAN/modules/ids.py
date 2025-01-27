from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from RAUSHAN import dev

@dev.on_message(filters.command("id"))
async def getid(client, message: Message):
    """
    نمایش شناسه‌های مختلف:
    - شناسه پیام
    - شناسه کاربر
    - شناسه چت
    - شناسه پیام پاسخ داده شده
    - شناسه کاربر پاسخ داده شده
    - شناسه کانال فوروارد شده
    - شناسه چت/کانال پاسخ داده شده
    """
    
    # دریافت اطلاعات اولیه
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    # ساخت متن پاسخ
    text = [
        f"**[شناسه پیام:]({message.link})** `{message_id}`",
        f"**[شناسه شما:](tg://user?id={your_id})** `{your_id}`"
    ]

    # بررسی دستور برای نمایش شناسه کاربر خاص
    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            # دریافت شناسه کاربر از نام کاربری یا شناسه
            split = message.text.split(None, 1)[1].strip()
            user = await client.get_users(split)
            text.append(
                f"**[شناسه کاربر:](tg://user?id={user.id})** `{user.id}`"
            )
        except Exception:
            return await message.reply_text(
                "این کاربر وجود ندارد.", 
                quote=True
            )

    # افزودن شناسه چت
    text.append(
        f"**[شناسه چت:](https://t.me/{chat.username})** `{chat.id}`\n"
    )

    # بررسی پیام پاسخ داده شده
    if (
        not getattr(reply, "empty", True)  # پیام پاسخ وجود دارد
        and not message.forward_from_chat  # پیام فوروارد نشده
        and not reply.sender_chat          # پیام از چت/کانال نیست
    ):
        text.extend([
            f"**[شناسه پیام پاسخ داده شده:]({reply.link})** `{reply.id}`",
            f"**[شناسه کاربر پاسخ داده شده:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n"
        ])

    # بررسی پیام فوروارد شده از کانال
    if reply and reply.forward_from_chat:
        text.append(
            f"کانال فوروارد شده {reply.forward_from_chat.title} "
            f"دارای شناسه `{reply.forward_from_chat.id}` است\n"
        )
        print(reply.forward_from_chat)  # نمایش اطلاعات کامل در کنسول

    # بررسی پیام از چت/کانال
    if reply and reply.sender_chat:
        text.append(
            f"شناسه چت/کانال پاسخ داده شده: `{reply.sender_chat.id}`"
        )
        print(reply.sender_chat)  # نمایش اطلاعات کامل در کنسول

    # ارسال پاسخ
    await message.reply_text(
        "\n".join(text),  # ترکیب خطوط با خط جدید
        disable_web_page_preview=True,  # غیرفعال کردن پیش‌نمایش لینک‌ها
        parse_mode=ParseMode.DEFAULT,   # استفاده از پارس مود پیش‌فرض
    )
