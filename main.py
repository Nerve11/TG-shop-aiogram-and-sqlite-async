import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
import threading
from db import init_db, add_user, increment_user_activity, log_message, log_blocked_message
from admin import register_admin_handlers
from shop import register_shop_handlers

API_TOKEN = "8100554424:AAFeTwBDdqChx-Yrf2O1BPiyQul-j5wgwMc"  #токен из ботфазер
logging.basicConfig(level=logging.INFO)

async def start_handler(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    await log_message(user_id, "online")  
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Магазин", callback_data="shop")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
    ])
    await message.answer("Привет! Я твой бот-магазин. Доступные команды:", reply_markup=keyboard)


async def help_handler(message: Message):
    user_id = message.from_user.id
    await log_message(user_id, "received") 
    await message.reply("Доступные команды: /start, /help, /shop, /admin")


async def echo_handler(message: Message):
    user_id = message.from_user.id
    await increment_user_activity(user_id)
    await log_message(user_id, "received")
    await message.reply(f"Вы сказали: {message.text}")

#errors
async def handle_errors(exception: Exception, user_id: int):
    if isinstance(exception, types.exceptions.BotBlocked):
        await log_blocked_message(user_id)  # Log


async def main():
    await init_db()

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()


    dp.message.register(start_handler, Command('start'))
    dp.message.register(help_handler, Command('help'))


    register_admin_handlers(dp)
    register_shop_handlers(dp)

    #echo если другие сообщения, но не ворк. яхз че как
    dp.message.register(echo_handler)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())