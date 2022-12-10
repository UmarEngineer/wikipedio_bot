from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

pdf = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='📘 PDF'),
        ]
    ],
    resize_keyboard=True
)