import logging

from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession

import time
import wikipedia
from config import API_TOKEN
from googletrans import Translator
from Wikipedia2PDF import Wikipedia2PDF
from pprint import pprint
from keyboards import pdf
from states import Holat

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

wikipedia.set_lang('uz')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(f"Assalomu aleykum, {message.from_user.full_name}!\n\nQidirayotgan maqolangiz uchun kalit so'zlarni kiriting yuboring yoki @wikipedio_bot so'zidan so'ng kalit so'zni yozing")    



@dp.message_handler()
# async def tarjima(message: types.Message):
#     translator =  Translator()
#     lang = translator.detect(message.text).lang
#     dest = 'uz' if lang == 'en' else 'uz'

#     word_id = translator.translate(message.text, dest=dest).text

async def sendWiki(message: types.Message):
    try:
        respond = wikipedia.page(message.text)
        respond2 = wikipedia.summary(message.text)
        global respond_url
        respond_url = respond.url
        more = f"\n\nBatafsil o'qish uchun bosing\n{respond.url}"
        await bot.send_photo(chat_id=message.from_user.id, photo=respond.images[0])
        if len(respond2) > 4096:
            for x in range(0, len(respond2), 4096):
                await bot.send_message(message.chat.id, f"{respond.title.upper()}\n\n{respond2[x:x+3950]} {more}")
        else:
            await message.answer(f"{respond.title.upper()}\n\n {respond2} {more}")
    
        # await bot.send_document(chat_id=message.from_user.id, document=Wikipedia2PDF(respond_url))

    except wikipedia.exceptions.DisambiguationError as e:
        option = ""
        k = 1
        for op in e.options:
            option += f"{k}. {op.title()}\n"
            k += 1
        await message.answer(f"Iltimos variantlardan birini tanlang\n\n{option}")
        logging.info(e) 


    except Exception as e:
        logging.info(e)
        await message.answer(f" Hurmatli <b>{message.from_user.full_name}</b> bot bilan bog'liq xato yuz berdi, qayta urunib ko'ring. \n\nYoki bu mavzuga oid o'zbek tilida maqola topilmadi.\nUshbu mavzuga oid maqola yozib O'zbek tilidagi Wikipedia rivojiga o'z hissangizni qo'sha olasiz. Shu bilan birga WikiMarafonda qatnashib pul yutug'lariga ham ega bo'lishingiz mumkin. WikiStipendiya haqida ba'tafsil ma'lumot olish uchun quyidagi manzilni ziyorat qiling: https://t.me/wikistipendiya \n\n \"Wikipedia siz kabi insonlar tomonidan yaratildi\"")
        # await message.answer(f"Hurmatli {message.from_user.full_name} afsuski, bu mavzu bo'yicha maqola topilmadi")

async def empty_query(query: types.InlineQuery):
    lang = translator.detect(message.text).lang
    
    if lang == 'en':
        word_id = translator.translate(message.text, dest='uz').text

    time.sleep(1)
    if not query.query == " ":
        try:
            que = wikipedia.search(query.query.lower(), results=3)
            resultSearch = []
            for qu in que:
                resultSearch.append(
                    types.InlineQueryResultArticle(
                        id=qu,
                        title=qu,
                        input_message_content=types.InputTextMessageContent(
                            message_text=qu
                        ),
                
                    )
                )
            await query.answer(
                resultSearch
            )
            # await State.inlineQuery.set()
        except wikipedia.exceptions.DisambiguationError as e:
            pprint(e.options)


    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
