from RAUSHAN import db

# دیتابیس گروه‌های ثبت شده
chatsdb = db.chatsdb


async def get_served_chats() -> list:
    """
    دریافت لیست تمام گروه‌های ثبت شده
    
    Returns:
        list: لیست گروه‌های ثبت شده
    """
    # جستجوی گروه‌ها (شناسه‌های منفی نشان‌دهنده گروه هستند)
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    
    # تبدیل نتایج به لیست
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    """
    بررسی ثبت شده بودن یک گروه
    
    Args:
        chat_id (int): شناسه گروه
        
    Returns:
        bool: True اگر گروه ثبت شده باشد، False در غیر این صورت
    """
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    """
    اضافه کردن یک گروه به لیست گروه‌های ثبت شده
    
    Args:
        chat_id (int): شناسه گروه
        
    Returns:
        pymongo.results.InsertOneResult: نتیجه درج در دیتابیس
    """
    # بررسی قبلاً ثبت شده بودن گروه
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    
    # افزودن گروه به دیتابیس
    return await chatsdb.insert_one({"chat_id": chat_id})


async def remove_served_chat(chat_id: int):
    """
    حذف یک گروه از لیست گروه‌های ثبت شده
    
    Args:
        chat_id (int): شناسه گروه
        
    Returns:
        pymongo.results.DeleteResult: نتیجه حذف از دیتابیس
    """
    # بررسی ثبت شده بودن گروه
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return
    
    # حذف گروه از دیتابیس
    return await chatsdb.delete_one({"chat_id": chat_id})
