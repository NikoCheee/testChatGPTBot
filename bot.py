from config import BOT_TOKEN
from openai_utils import create_answer
from aiogram import Bot, types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import asyncio
import logging
from datetime import datetime

token = BOT_TOKEN

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot)
print("Бот запущений")

# Configure logging
logging.basicConfig(filename='log.txt', encoding='UTF-8', format="%(asctime)s %(funcName)s: %(message)s")


@dp.message_handler(commands=['start'])
async def start_command_handler(message: Message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {message.from_user.full_name} написав старт")
    await message.answer(f'Привіт, {message.from_user.full_name}! Я бот, через якого можна спитати '
                         f'що завгодно у чата GPT. Тож питай, не соромся!')


@dp.message_handler()
async def gpt_handler(message: Message):
    try:
        text = message.text
        print(f"{datetime.now().strftime('%H:%M:%S')} {message.from_user.full_name} зробив запрос у чат жпт")

        answer_task = asyncio.create_task(create_answer(text))
        wait_task = asyncio.create_task(waiting(message))

        answer = await answer_task
        if answer_task.done():
            wait_task.cancel()
            await message.answer(answer)
        await wait_task
        print(f"{datetime.now().strftime('%H:%M:%S')} {message.from_user.full_name} отримав відповідь")
    except Exception as e:
        logging.error(e)
        await message.answer("На жаль, під час виконання запиту сталася помилка. Спробуйте ще раз пізніше.")


@dp.message_handler()
async def waiting(msg: Message):
    print(f"{datetime.now().strftime('%H:%M:%S')} очікуюча функція викликалась")
    await asyncio.sleep(4)
    while True:
        await bot.send_message(msg.from_user.id, '<i>Хвилинку...</i>')
        print(f"{datetime.now().strftime('%H:%M:%S')}")
        await asyncio.sleep(8)
        await bot.send_message(msg.from_user.id, 'Зачекайте ще трохи...')
        await asyncio.sleep(12)
        await bot.send_message(msg.from_user.id, 'І ще трохи...')
        print(f'{datetime.now().strftime("%H:%M:%S")}')


if __name__ == '__main__':
    try:
        # executor.start_polling(dp)
        asyncio.run(executor.start_polling(dp))
    except Exception as e:
        logging.error(e)
