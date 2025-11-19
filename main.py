import asyncio
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import firebase_admin
from firebase_admin import credentials, firestore

# === BOT TOKEN ===
API_TOKEN = '8369431718:AAGcq9txjvE5PK0YFmuKUrr-iNHvEc65Xy4'

# === FIREBASE ===
# Environment variable dan JSON stringni o'qish
service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if not service_account_json:
    raise RuntimeError("❌ Environment variable FIREBASE_SERVICE_ACCOUNT topilmadi!")

service_account_info = json.loads(service_account_json)
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
db = firestore.client()

# === BOT ===
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# /start komandasi
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

# Kontakt orqali kelgan raqamni qabul qilish
@dp.message(lambda msg: msg.contact is not None)
async def contact_handler(message: types.Message):
    phone = message.contact.phone_number
    user_id = message.from_user.id

    # Firestore-ga saqlash
    db.collection("users").document(str(user_id)).set({
        "user_id": user_id,
        "phone": phone
    })

    # Mini app linkini yuborish
    mini_app_url = "https://stirring-sunflower-b75418.netlify.app/"
    await message.answer(
        f"✅ Ma'lumotlaringiz saqlandi!\n\n"
        f"Endi ilovamizni ochishingiz mumkin mini app sifatida:\n"
        f"{mini_app_url}"
    )

# Qo‘lda yozilgan raqamlarni rad qilish
@dp.message(lambda msg: msg.text and msg.contact is None)
async def reject_text(message: types.Message):
    await message.answer("❗ Iltimos raqamni qo‘lda yozmang. Pastdagi tugmani bosing 👇")

# === Asosiy loop ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
