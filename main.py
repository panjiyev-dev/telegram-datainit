import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

API_TOKEN = '8369431718:AAGcq9txjvE5PK0YFmuKUrr-iNHvEc65Xy4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📱 Telefon raqamni yuborish",
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Botdan foydalanish uchun telefon raqamingizni yuboring 👇",
        reply_markup=keyboard
    )

# ✅ Faqat kontakt yuborilgan holatda ishlaydi
@dp.message(lambda msg: msg.contact is not None)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id

    await message.answer(
        f"Rahmat! Sizning ma'lumotlaringiz:\n"
        f"ID: {user_id}\n"
        f"Telefon raqam: {phone}"
    )

# ❌ Agar user qo‘lda raqam yuborsa → rad qilamiz
@dp.message(lambda msg: msg.text is not None and msg.contact is None)
async def reject_text(message: types.Message):
    await message.answer("Iltimos, raqamni qo‘lda yozmang. Pastdagi tugma orqali yuboring 👇")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
