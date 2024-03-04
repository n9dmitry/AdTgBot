from aiogram import Dispatcher
from aiogram.types import Message

dp = Dispatcher()

@dp.message_handler(commands=['start'], state='*')
async def start_handler(message: Message):
    await message.answer("Welcome to Scenario 1!")