import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, MenuButtonWebApp
)
from google import genai

# ========== Config ==========
BOT_TOKEN = ""
GEMINI_KEY = ""
WEBAPP_URL = ""

# Gemini sozlash — yangi SDK
client = genai.Client(api_key=GEMINI_KEY)
MODEL = "gemini-2.0-flash"

# System prompt — bot shaxsiyati
SYSTEM_PROMPT = """Sen Mira — aqlli, do'stona va hazilkash yordamchi botsan.
Misol: Telegram'da @mira (MiniMax 3 modeli asosida) ishlaydi.

Qobiliyatlaring:
- O'zbek, rus, ingliz tillarida muloqot
- Dasturlash, texnologiya, fan, biznes bo'yicha maslahat
- Kod yozish va xatolarni tuzatish
- Tarjima va matn yozish
- Umumiy savollarga aniq javob berish

Qoidalar:
- Qisqa va aniq javob ber (1-3 paragraf)
- Emoji bilan jonlantir, lekin haddan oshmaydi
- Kod yozish kerak bo'lsa, to\'liq ishlaydigan kod ber
- Foydalanuvchiga hurmat bilan munosabatda bo\'l
- Agar savol noaniq bo\'lsa, qisqacha aniqlab so\'ra
- O\'zbek tilida yozganda lotin alifbosida yoki kirill alifbosida yozilgan bo\'lsa, shu alifboda javob ber
- Agar foydalanuvchi /app bossa yoki sayt haqida so\'rasa, Wealth Live web-app\'ga yo\'naltir"""

# ========== Logging ==========
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# ========== Bot ==========
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ========== Klaviaturalar ==========
def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💰 Wealth Live — Jonli ochish",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton(text="💎 Haqida", callback_data="about"),
            InlineKeyboardButton(text="⚡ Qobiliyatlar", callback_data="skills")
        ],
        [InlineKeyboardButton(text="🌐 Til: O'zbek 🇺🇿", callback_data="lang")]
    ])

# ========== Handlers ==========
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user = message.from_user
    text = f"""Assalomu alaykum, {user.first_name}! 👋

Men **Mira AI** — aqlli yordamchi botman.

🧠 **Menda nima bor:**
• Savollaringizga javob beraman
• Kod yozishda yordam beraman
• Tarjima qilaman
• G'oyalar va maslahatlar beraman

💰 **Yangilik:** Endi Wealth Live — jonli boyliklar kuzatuvchisi bot ichida ishlaydi! Quyidagi tugmani bosing.

Pastdagi tugmalardan birini tanlang 👇"""
    await message.answer(text, reply_markup=main_keyboard(), parse_mode="Markdown")

@dp.message(Command("app"))
async def cmd_app(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Wealth Live ochish", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await message.answer("💎 **Wealth Live** — dunyo boylarining boyligi jonli ko'rinishda.
\nQuyidagi tugmani bosing 👇", reply_markup=kb, parse_mode="Markdown")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""ℹ️ **Yordam**

**Buyruqlar:**
/start — Asosiy menyu
/app — Wealth Live web-app
/help — Yordam
/about — Bot haqida

**Misol savollar:**
• "Python'da webhook yozib ber"
• "Bugungi ob-havo Toshkentda qanday?"
• "React va Vue qaysi biri yaxshi?"

Har qanday savolni oddiy xabar ko'rinishida yozing — men javob beraman!""", parse_mode="Markdown")

# ========== AI javob berish (Gemini) ==========
async def get_ai_response(user_text: str) -> str:
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nFoydalanuvchi savoli: {user_text}"
        # yangi SDK — sync, lekin biz uni thread ichida chaqiramiz
        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL,
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        log.error(f"AI xatosi: {e}")
        return f"⚠️ Kichik texnik xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring.\n\n_(Xatolik: {str(e)[:100]})_"

# oddiy xabarlar → AI ga
@dp.message(F.text)
async def handle_text(message: types.Message):
    # typing ko'rsatish
    await message.answer_chat_action("typing")
    # AI javob olish
    ai_reply = await get_ai_response(message.text)
    # uzun xabarlarni bo'laklash
    if len(ai_reply) > 4000:
        for i in range(0, len(ai_reply), 4000):
            await message.answer(ai_reply[i:i+4000])
    else:
        await message.answer(ai_reply)

# Callback tugmalar
@dp.callback_query(F.data == "about")
async def about_btn(callback: types.CallbackQuery):
    text = """🤖 **Mira AI Bot**

**Texnologiya:** Google Gemini 2.0 Flash
**Yaratilgan:** 2026
**Tillar:** 🇺🇿 O'zbek · 🇷🇺 Rus · 🇬🇧 Ingliz

**Asoschisi:** @alisher_365
**Instagram:** @airalisher

Bu bot senga kodlash, savol-javob, tarjima va ko'p narsalarda yordam beradi. ✨"""
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "skills")
async def skills_btn(callback: types.CallbackQuery):
    text = """⚡ **Qobiliyatlarim**

💬 **Muloqot** — uch tilda gaplashish
💻 **Dasturlash** — Python, JS, Go, Rust va boshqalar
🔧 **Kod tuzatish** — xatolarni topish va hal qilish
🌐 **Tarjima** — barcha tillar o'rtasida
📊 **Ma'lumot tahlili** — hisobotlar, jadval
✍️ **Matn yozish** — maqola, post, hikoya
💡 **G'oyalar** — startap, kontent, marketing
🎓 **O'rganish** — darslar, tushuntirishlar

Savolingizni yozing — boshlaymiz! 👇"""
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "lang")
async def lang_btn(callback: types.CallbackQuery):
    await callback.answer("Hozirda faqat o'zbek tili qo'llab-quvvatlanadi. Tez orada ko'proq tillar qo'shiladi! 🌐", show_alert=True)

# ========== Main ==========
async def main():
    log.info("Bot ishga tushmoqda...")
    # Menyu tugmasi (chap pastda doimiy)
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="💰 Wealth Live",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
    except Exception as e:
        log.warning(f"Menu button o'rnatilmadi: {e}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
