# 🤖 Mira AI Bot

Telegram bot — Google Gemini 2.0 Flash bilan ishlaydi. Web-app sifatida Wealth Live (billionaire tracker) ulangan.

## ⚙️ Tez o'rnatish

### 1. Python o'rnatish
Python 3.10+ kerak. [python.org](https://python.org) dan yuklab oling.

### 2. Kutubxonalar
```bash
cd /home/user/bot
pip install -r requirements.txt
```

### 3. Botni ishga tushirish
```bash
python bot.py
```

Yoki **24/7 ishlashi uchun** quyidagi bepul hostinglardan birini tanlang:

## 🚀 Bepul hosting (24/7 ishlashi uchun)

### Variant A: **Render.com** (eng oson)
1. [render.com](https://render.com) da ro'yxatdan o'ting
2. **New +** → **Web Service** (yoki Background Worker)
3. GitHub repo ulang yoki **Public Git repository** URL kiriting
4. Sozlamalar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Plan:** Free
5. **Environment** bo'limiga qo'ying:
   - `BOT_TOKEN` = `8907069405:AAEY3nWaLYUqprr4pgomVwtwwrCXxFl6FRc`
   - `GEMINI_KEY` = `AQ.Ab8RN6JJd4kQGJKZaDtukptp5DJO_vFvKASdsUX2DhHcwGqedA`

### Variant B: **Railway.app** (tezroq)
1. [railway.app](https://railway.app) ga kiring
2. **New Project** → **Deploy from GitHub repo**
3. **Variables** bo'limiga token va key qo'ying
4. Deploy avtomatik boshlanadi

### Variant C: **VPS** (to'liq nazorat)
- Hetzner, DigitalOcean, yoki Contabo (oyiga $4-5)
- SSH orqali ulanib, `screen` yoki `systemd` bilan ishga tushiring

## 🔒 Xavfsizlik
- Bot token va API key ni **GitHub'ga public qilmang**
- `.env` fayl yarating yoki hosting platformasining **Environment Variables** dan foydalaning

## 📋 Buyruqlar
- `/start` — asosiy menyu
- `/app` — Wealth Live web-app ochish
- `/help` — yordam

## 💡 Qo'shimcha
- **Webhook** rejimiga o'tkazish mumkin (tezroq, lekin hosting URL kerak)
- **Ma'lumotlar bazasini** qo'shish mumkin (foydalanuvchi tarixini saqlash)
- **Guruhlar** uchun ham sozlash mumkin

