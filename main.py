import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

API_TOKEN = '8369431718:AAGcq9txjvE5PK0YFmuKUrr-iNHvEc65Xy4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍃 WebApp ochish",
                    web_app=WebAppInfo(url="https://starlit-sorbet-de9046.netlify.app/")
                )
            ]
        ]
    )

    await message.answer(
        "WebApp ochish uchun pastdagi tugmani bosing 👇",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
