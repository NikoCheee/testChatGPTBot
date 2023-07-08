from config import BOT_TOKEN, OpenAIToken, my_api
from aiogram import Bot, types
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import asyncio
import logging
import openai
from datetime import datetime

token = BOT_TOKEN
openai.api_key = my_api

bot = Bot(token)
dp = Dispatcher(bot)
print("Бот запущений")


@dp.message_handler(commands=['start'])
async def start_command_handler(message: Message):
    print(f"{datetime.now().strftime('%H:%M:%S')} {message.from_user.full_name} написав старт")
    await message.answer(f'Привіт, {message.from_user.full_name}! Я бот, через якого можна спитати '
                         f'що завгодно у чата GPT. Тож питай, не соромся!')


@dp.message_handler()
async def gpt_handler(message: Message):
    text = message.text
    print(f"{datetime.now().strftime('%H:%M:%S')} {message.from_user.full_name} зробив запрос у чат жпт")

    # answer = await create_answer(text)
    answer = await asyncio.gather(create_answer(text), waiting())

    await message.answer(answer[0])
    print(f"{datetime.now().strftime('%H:%M:%S')} {message.from_user.full_name} отримав відповідь")


@dp.message_handler()
async def waiting():  # send messages
    print(f"{datetime.now().strftime('%H:%M:%S')} очікуюча функція викликалась")
    print(f"{datetime.now().strftime('%H:%M:%S')} Зачекайте трохи...")
    await asyncio.sleep(5)
    print(f'{datetime.now().strftime("%H:%M:%S")} Зачекайте ще трохи...')


async def create_answer(text):  # TODO системне повідомлення
    answer = await __get_gpt_completion(text=text)
    return answer


async def __get_gpt_completion(text):  # TODO системне повідомлення
    print(f'{datetime.now().strftime("%H:%M:%S")} зараз буде запускатись гет_гпт_комп')
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # TODO налаштувати
            {"role": "user", "content": f"{text}"}
        ]
    )

    print(f"{datetime.now().strftime('%H:%M:%S')} запрос для '{text[:15]}' оброблено")
    answer = completion.choices[0].message
    return answer['content']


if __name__ == '__main__':
    # executor.start_polling(dp)
    asyncio.run(executor.start_polling(dp))
