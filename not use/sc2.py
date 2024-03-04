from aiogram import Dispatcher
from aiogram.types import Message

dp = Dispatcher()

@dp.message_handler(commands=['help'], state='*')
async def help_handler(message: Message):
    await message.answer("Help message for Scenario 2")
