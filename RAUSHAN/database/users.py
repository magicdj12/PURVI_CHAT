from RAUSHAN import db

# دیتابیس کاربران
usersdb = db.users


async def is_served_user(user_id: int) -> bool:
    """
    بررسی ثبت شده بودن یک کاربر
    
    Args:
        user_id (int): شناسه کاربر
        
    Returns:
        bool: True اگر کاربر ثبت شده باشد، False در غیر این صورت
    """
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    """
    دریافت لیست تمام کاربران ثبت شده
    
    Returns:
        list: لیست کاربران ثبت شده
    """
    users_list = []
    # جستجوی کاربران (شناسه‌های مثبت نشان‌دهنده کاربر هستند)
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    """
    اضافه کردن یک کاربر به لیست کاربران ثبت شده
    
    Args:
        user_id (int): شناسه کاربر
        
    Returns:
        pymongo.results.InsertOneResult: نتیجه درج در دیتابیس
    """
    # بررسی قبلاً ثبت شده بودن کاربر
    is_served = await is_served_user(user_id)
    if is_served:
        return
    
    # افزودن کاربر به دیتابیس
    return await usersdb.insert_one({"user_id": user_id})
