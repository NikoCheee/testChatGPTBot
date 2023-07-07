from config import BOT_TOKEN, OpenAIToken, my_api
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import logging
import openai

token = BOT_TOKEN
openai.api_key = my_api

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command_handler(message: Message):
    await message.answer(f'Привіт, {message.from_user.full_name}! Я бот, через якого можна спитати '
                         f'що завгодно у чата GPT. Тож питай, не соромся!')


@dp.message_handler()
async def echo_handler(message: Message):
    text = message.text

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful asistant."},  # налаштувати
            {"role": "user", "content": f"{text}"}
        ]
    )

    answer = completion.choices[0].message

    await message.answer(answer['content'])


if __name__ == '__main__':
    executor.start_polling(dp)