import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from RAUSHAN import OWNER, dev

# اجرای کد پایتون به صورت async
async def aexec(code, client, message):
    """کد پایتون را به صورت async اجرا می‌کند"""
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

# ویرایش یا پاسخ به پیام
async def edit_or_reply(msg: Message, **kwargs):
    """پیام را ویرایش یا به آن پاسخ می‌دهد"""
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})

# دستور eval برای اجرای کد پایتون
@dev.on_edited_message(
    filters.command("eval") & filters.user(OWNER) & ~filters.forwarded & ~filters.via_bot
)
@dev.on_message(
    filters.command("eval") & filters.user(OWNER) & ~filters.forwarded & ~filters.via_bot
)
async def executor(client: dev, message: Message):
    """دستور eval برای اجرای کد پایتون"""
    if len(message.command) < 2:
        return await edit_or_reply(message, text="چه کدی می‌خواهید اجرا کنید؟")

    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()

    # ذخیره خروجی‌ها
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None

    # اجرای کد
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    # دریافت خروجی‌ها
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    # آماده‌سازی خروجی نهایی
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "موفقیت‌آمیز"

    final_output = f"<b>⥤ نتیجه:</b>\n<pre language='python'>{evaluation}</pre>"

    # ارسال خروجی
    if len(final_output) > 4096:
        # اگر خروجی طولانی باشد، در فایل ذخیره می‌شود
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="⏳",
                callback_data=f"runtime {t2-t1} Seconds"
            )]
        ])
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ کد:</b>\n<code>{cmd[0:980]}</code>\n\n<b>⥤ نتیجه:</b>\nفایل پیوست",
            quote=False,
            reply_markup=keyboard
        )
        await message.delete()
        os.remove(filename)
    else:
        # ارسال مستقیم خروجی
        t2 = time()
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="⏳",
                    callback_data=f"runtime {round(t2-t1, 3)} Seconds"
                ),
                InlineKeyboardButton(
                    text="🗑",
                    callback_data=f"forceclose abc|{message.from_user.id}"
                )
            ]
        ])
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)

# پاسخ به دکمه‌های زمان اجرا
@dev.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    """نمایش زمان اجرای کد"""
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)

# پاسخ به دکمه بستن
@dev.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    """بستن پیام خروجی"""
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "این دکمه برای شما نیست!", show_alert=True
            )
        except:
            return
            
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return

# دستور shell برای اجرای دستورات سیستمی
@dev.on_edited_message(
    filters.command("sh") & filters.user(OWNER) & ~filters.forwarded & ~filters.via_bot
)
@dev.on_message(
    filters.command("sh") & filters.user(OWNER) & ~filters.forwarded & ~filters.via_bot
)
async def shellrunner(client: dev, message: Message):
    """اجرای دستورات shell"""
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>مثال:</b>\n/sh git pull")

    text = message.text.split(None, 1)[1]
    
    if "\n" in text:
        # اجرای چند دستور
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                return await edit_or_reply(message, text=f"<b>خطا:</b>\n<pre>{err}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        # اجرای یک دستور
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"<b>خطا:</b>\n<pre>{''.join(errors)}</pre>"
            )
        output = process.stdout.read()[:-1].decode("utf-8")

    if str(output) == "\n":
        output = None
        
    if output:
        if len(output) > 4096:
            # ارسال خروجی طولانی در فایل
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>خروجی</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>خروجی:</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>خروجی:</b>\n<code>خالی</code>")
