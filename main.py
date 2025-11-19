import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import firebase_admin
from firebase_admin import credentials, firestore

API_TOKEN = '8369431718:AAGcq9txjvE5PK0YFmuKUrr-iNHvEc65Xy4'

# === FIREBASE ===
cred = credentials.Certificate("FIREBASE_SERVICE_ACCOUNT")  # Firebase JSON
firebase_admin.initialize_app(cred)
db = firestore.client()

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

# 🔥 Kontakt orqali kelgan raqamni qabul qilish
@dp.message(lambda msg: msg.contact is not None)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id

    # Firestorega saqlash
    db.collection("users").document(str(user_id)).set({
        "user_id": user_id,
        "phone": phone
    })

    await message.answer(
        f"Rahmat! Ma'lumotlar saqlandi:\n"
        f"ID: {user_id}\n"
        f"Telefon: {phone}"
    )

# ❌ Qo‘lda yozilgan matnni rad qilish
@dp.message(lambda msg: msg.text and msg.contact is None)
async def reject_text(message: types.Message):
    await message.answer("❗ Iltimos raqamni qo‘lda yozmang. Pastdagi tugmani bosing 👇")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
