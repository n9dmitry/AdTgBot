from aiogram import Dispatcher
from aiogram.types import Message

dp = Dispatcher()

@dp.message_handler(commands=['about'], state='*')
async def about_handler(message: Message):
    await message.answer("About Scenario 3")
