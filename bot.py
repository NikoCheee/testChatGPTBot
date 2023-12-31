from config import BOT_TOKEN
from openai_utils import create_answer
from utils import get_random_waiting_phrase
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import asyncio
import logging

token = BOT_TOKEN

bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot)
print("Бот запущений")

# Configure logging
logging.basicConfig(filename='log.txt', encoding='UTF-8',
                    format="%(asctime)s %(funcName)s: %(message)s")


@dp.message_handler(commands=['start'])
async def start_command_handler(message: Message):
    await message.answer(f'Привіт, {message.from_user.full_name}! Я бот, через якого можна спитати '
                         f'що завгодно у чата GPT. Тож питай, не соромся!')


@dp.message_handler(commands=['help'])
async def help_command_handler(message: Message):
    await message.answer('Я чат бот, побудований на бібліотеці aiogram, який звертається до OpenAI API.\n'
                         'Моя модель "gpt-3.5-turbo", а моя сутність вкладається у "You are a helpful assistant". '
                         'На жаль поки це змінити неможливо, але у майбутньому... Так що приємного користування!')


@dp.message_handler()
async def gpt_handler(message: Message):
    try:
        text = message.text

        answer_task = asyncio.create_task(create_answer(text))
        wait_task = asyncio.create_task(waiting(message))

        answer = await answer_task
        if answer_task.done():
            wait_task.cancel()
            await message.answer(answer)
        await wait_task

    except Exception as e:
        logging.error(e)
        # answer_task.cancel()
        wait_task.cancel()
        await message.answer("На жаль, під час виконання запиту сталася помилка. Спробуйте ще раз пізніше.")


@dp.message_handler()
async def waiting(msg: Message, first_wait=4, delay=10):
    """
    Function for sending waiting phrases while openai api processing request.
    Random phrases generates from outer function get_random_waiting_phrase().
    :param msg: message to get chat id, type of tg Message
    :param first_wait: waiting time for first waiting phrase, default=4
    :param delay: waiting time between other waiting phrases, default=10
    :return:
    """
    await asyncio.sleep(first_wait)
    while True:
        test = await get_random_waiting_phrase()
        await bot.send_message(msg.from_user.id, f'{test}')
        await asyncio.sleep(delay)


if __name__ == '__main__':
    try:
        asyncio.run(executor.start_polling(dp))
    except Exception as e:
        logging.error(e)
