import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, Text

API_TOKEN = '8369431718:AAGcq9txjvE5PK0YFmuKUrr-iNHvEc65Xy4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Telefon raqamini yuborish tugmasi bilan klaviatura
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Telefon raqamni yuborish",
                    request_contact=True  # Telefon raqamini so'rash
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Botdan foydalanish uchun telefon raqamingizni yuboring 👇",
        reply_markup=keyboard
    )

@dp.message(Text(), lambda message: message.contact is not None)
async def contact_handler(message: types.Message):
    contact = message.contact
    user_id = message.from_user.id
    phone_number = contact.phone_number

    # Foydalanuvchi ID va telefon raqamini qaytarish
    await message.answer(
        f"Rahmat! Sizning ma'lumotlaringiz:\n"
        f"Foydalanuvchi ID: {user_id}\n"
        f"Telefon raqam: {phone_number}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
