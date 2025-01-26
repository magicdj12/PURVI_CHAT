from pyrogram.types import InlineKeyboardButton
from config import SUPPORT_GRP, UPDATE_CHNL
from RAUSHAN import BOT_USERNAME, OWNER

DEV_OP = [
    [
        InlineKeyboardButton(
            text="➕ افزودن به گروه",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="👨‍💻 سازنده", user_id=OWNER),
        InlineKeyboardButton(text="💡 راهنما و دستورات", callback_data="HELP"),
    ],
]

PNG_BTN = [
    [
        InlineKeyboardButton(
            text="➕ افزودن به گروه",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(
            text="❌ بستن",
            callback_data="CLOSE",
        ),
    ],
]

BACK = [
    [
        InlineKeyboardButton(text="🔙 برگشت", callback_data="BACK"),
    ],
]

HELP_BTN = [
    [
        InlineKeyboardButton(text="🤖 چت‌بات", callback_data="CHATBOT_CMD"),
        InlineKeyboardButton(text="🛠 ابزارها", callback_data="TOOLS_DATA"),
    ],
    [
        InlineKeyboardButton(text="🔙 برگشت", callback_data="BACK"),
        InlineKeyboardButton(text="❌ بستن", callback_data="CLOSE"),
    ],
]

CLOSE_BTN = [
    [
        InlineKeyboardButton(text="❌ بستن", callback_data="CLOSE"),
    ],
]

CHATBOT_ON = [
    [
        InlineKeyboardButton(text="✅ فعال‌سازی", callback_data=f"addchat"),
        InlineKeyboardButton(text="❌ غیرفعال‌سازی", callback_data=f"rmchat"),
    ],
]

MUSIC_BACK_BTN = [
    [
        InlineKeyboardButton(text="🔜 به‌زودی", callback_data=f"soom"),
    ],
]

S_BACK = [
    [
        InlineKeyboardButton(text="🔙 برگشت", callback_data="SBACK"),
        InlineKeyboardButton(text="❌ بستن", callback_data="CLOSE"),
    ],
]

CHATBOT_BACK = [
    [
        InlineKeyboardButton(text="🔙 برگشت", callback_data="CHATBOT_BACK"),
        InlineKeyboardButton(text="❌ بستن", callback_data="CLOSE"),
    ],
]

HELP_START = [
    [
        InlineKeyboardButton(text="💡 راهنما", callback_data="HELP"),
        InlineKeyboardButton(text="❌ بستن", callback_data="CLOSE"),
    ],
]

HELP_BUTN = [
    [
        InlineKeyboardButton(
            text="💡 راهنما", url=f"https://t.me/{BOT_USERNAME}?start=help"
        ),
        InlineKeyboardButton(text="❌ بستن", callback_data="CLOSE"),
    ],
]

ABOUT_BTN = [
    [
        InlineKeyboardButton(text="👥 پشتیبانی", url=f"https://t.me/{SUPPORT_GRP}"),
        InlineKeyboardButton(text="💡 راهنما", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="👨‍💻 سازنده", user_id=OWNER),
        InlineKeyboardButton(text="ℹ️ سورس", callback_data="SOURCE"),
    ],
    [
        InlineKeyboardButton(text="📢 کانال آپدیت‌ها", url=f"https://t.me/{UPDATE_CHNL}"),
        InlineKeyboardButton(text="🔙 برگشت", callback_data="BACK"),
    ],
]
