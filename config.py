from os import getenv
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()

# تنظیمات اصلی ربات
API_ID = int(getenv("API_ID", "21803165"))  # شناسه API تلگرام
API_HASH = getenv("API_HASH", "05e5e695feb30e25bef47484cc006da7")  # هش API تلگرام
BOT_TOKEN = getenv("BOT_TOKEN", None)  # توکن ربات
OWNER_ID = int(getenv("OWNER_ID", "7154410907"))  # شناسه مالک ربات
MONGO_URL = getenv("MONGO_URL", None)  # آدرس اتصال به پایگاه داده مونگو

# تنظیمات کانال‌ها و پشتیبانی
SUPPORT_GRP = getenv("SUPPORT_GRP", "Poshtibaninetroplusbot")  # گروه پشتیبانی
UPDATE_CHNL = getenv("UPDATE_CHNL", "me_nitroplus")  # کانال آپدیت‌ها
OWNER_USERNAME = getenv("OWNER_USERNAME", "Owner_nitroplus")  # نام کاربری مالک

# تصاویر تصادفی شروع
IMG = [
    "https://telegra.ph/file/00eb565274ccbffcf149d.jpg",
    "https://telegra.ph/file/396e2af77c4664164de18.jpg",
    "https://telegra.ph/file/6f92a0e943d68a15169c0.jpg",
    "https://telegra.ph/file/d49fbf4c00f839641afe3.jpg",
    "https://telegra.ph/file/cdcdceb3d4fc34675b815.jpg",
    "https://telegra.ph/file/cc6259af790c13f98c38c.jpg",
    "https://telegra.ph/file/ffa18225730df716d3532.jpg",
    "https://telegra.ph/file/dc051f4160954159675a2.jpg",
    "https://telegra.ph/file/e0e0a3f2addbf58b943e8.jpg",
    "https://telegra.ph/file/2e6d9db59c537c4521440.jpg",
    "https://telegra.ph/file/f1951920bbd57921d8820.jpg",
    "https://telegra.ph/file/ece475f9a419442c18f1d.jpg",
    "https://telegra.ph/file/99a0014129f08eb1a44dc.jpg",
    "https://telegra.ph/file/ac8e3751509cf4e1b4756.jpg",
    "https://telegra.ph/file/e07ef19b1f9bbde9909ad.jpg",
    "https://telegra.ph/file/d3ee41261ed7779f30a89.jpg",
]

# استیکرهای تصادفی
STICKER = [
    "CAACAgEAAxkBAAIJomRdLhVJVebkx0JRsp1STwTv3t3eAAJrAgAClpxhRD4z4bgqlIF0LwQ",
    "CAACAgUAAxkBAAIJo2RdLhjLjCpmPipMT8ksrqwUjGAIAAK1BQACLZ8oVFVNmhalU8eOLwQ",
    "CAACAgUAAxkBAAIJpGRdLkpU7t2WDj9zUFgCJ5uHUdGHAALTBAAC59CYV3t9x-f0tt4OLwQ",
]

# ایموجی‌های تصادفی
EMOJIOS = [
    "🎲",  # تاس
    "🔥",  # آتش
    "⚡️",  # رعد و برق
    "⛈",   # ابر و باران
    "🌩",  # ابر و رعد و برق
    "🌦",  # ابر و خورشید و باران
    "☀️",  # خورشید
    "💫",  # ستاره درخشان
    "🐳",  # نهنگ
    "🦑",  # اختاپوس
]
