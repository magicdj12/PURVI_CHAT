import asyncio
import importlib
import logging
import re
import sys
import time

from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client

import config
from RAUSHAN.modules import all_modules

# تنظیمات لاگینگ
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ],
    level=logging.INFO,
)

# کاهش سطح لاگ‌های pyrogram
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# متغیرهای اصلی
boot = time.time()  # زمان شروع ربات

# اتصال به دیتابیس
mongo = MongoCli(config.MONGO_URL)
db = mongo.Anonymous

# تنظیمات دسترسی
OWNER = config.OWNER_ID
# DEVS = config.SUDO_USERS | config.OWNER_ID


class AMBOT(Client):
    """
    کلاس اصلی ربات که از Client پایروگرام ارث‌بری می‌کند
    """
    def __init__(self):
        """
        مقداردهی اولیه کلاس ربات
        """
        super().__init__(
            name="AMBOT",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="RAUSHAN.modules"),
        )

    async def start(self):
        """
        شروع ربات و دریافت اطلاعات آن
        """
        await super().start()
        get_me = await self.get_me()
        
        # ذخیره اطلاعات ربات
        self.id = get_me.id
        self.name = get_me.mention
        self.username = get_me.username
        
        LOGGER.info(f"ربات {self.name} شروع به کار کرد")

    async def stop(self):
        """
        توقف ربات
        """
        await super().stop()
        LOGGER.info("ربات متوقف شد")


# ایجاد نمونه برای توسعه
dev = Client(
    "Dev",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    # plugins=dict(root="RAUSHAN.modules"),
)

# شروع کلاینت توسعه
dev.start()

# دریافت اطلاعات ربات
BOT_ID = config.BOT_TOKEN.split(":")[0]
bot_info = dev.get_me()
BOT_NAME = bot_info.first_name + (bot_info.last_name or "")
BOT_USERNAME = bot_info.username
BOT_MENTION = bot_info.mention
BOT_DC_ID = bot_info.dc_id

LOGGER.info(f"""اطلاعات ربات:
نام: {BOT_NAME}
نام کاربری: @{BOT_USERNAME}
شناسه: {BOT_ID}
دیتاسنتر: {BOT_DC_ID}
""")
