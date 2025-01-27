from flask import Flask
import threading
from RAUSHAN import LOGGER, AMBOT

# ایجاد نمونه از برنامه Flask
app = Flask(__name__)

@app.route("/")
def home():
    """
    مسیر اصلی وب سرور
    
    Returns:
        str: پیام وضعیت ربات
    """
    return "ربات در حال اجرا است"

def run_flask():
    """
    راه‌اندازی سرور Flask
    
    این تابع سرور وب را روی پورت 8000 اجرا می‌کند
    و به همه آدرس‌های IP اجازه دسترسی می‌دهد
    """
    app.run(
        host="0.0.0.0",  # اجازه دسترسی از همه آدرس‌های IP
        port=8000        # پورت سرور
    )

def run_bot():
    """
    راه‌اندازی ربات تلگرام
    
    این تابع ربات اصلی را راه‌اندازی می‌کند و
    یک پیام لاگ برای شروع کار ثبت می‌کند
    """
    LOGGER.info("ربات چت PURVI شروع به کار کرد.")
    AMBOT().run()

if __name__ == "__main__":
    try:
        # ایجاد thread برای اجرای سرور Flask
        flask_thread = threading.Thread(
            target=run_flask,
            name="FlaskThread"
        )
        flask_thread.daemon = True  # thread به صورت daemon اجرا می‌شود
        flask_thread.start()
        
        LOGGER.info("سرور وب Flask راه‌اندازی شد")
        
        # اجرای ربات در thread اصلی
        run_bot()
        
    except Exception as e:
        LOGGER.error(f"خطا در راه‌اندازی برنامه: {str(e)}")
        raise
