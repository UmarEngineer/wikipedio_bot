import logging

from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession

from config import API_TOKEN
from keyboards import book_keyboard, recent_books_list

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Assalomu aleykum, {message.from_user.full_name}!\n\nQidirayotgan maqolangiz uchun kalit so'zlarni kiriting yuboring yoki @wikipedio_bot so'zidan so'ng kalit so'zni yozing")    
