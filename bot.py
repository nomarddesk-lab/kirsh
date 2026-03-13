import os
import threading
import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- Web Server for Render.com Health Checks ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Premium Gold AI Agent Active", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Configuration & Redirect ---
CHANNEL_URL = "https://t.me/KIRSH_GOLD_SIGNALS"
SYSTEM_LOG = "<code>[SISTEM IA]:</code>"

# --- Bot Logic ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium Welcome in Malay with AI Terminal feel."""
    user_name = update.effective_user.first_name
    
    # Premium Menu Layout
    keyboard = [
        ["🚀 AKSES SIGNAL EMAS"],
        ["📊 ANALISIS PASARAN", "💎 JOIN VIP GRATIS"],
        ["📞 HUBUNGI ADMIN"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        f"🤖 <b>TERMINAL IA KIRSH GOLD</b>\n"
        f"————————————————————\n"
        f"Selamat datang, <b>{user_name}</b>. Enkripsi sistem aktif.\n\n"
        f"<code>> Mengimbas kecairan pasaran...</code>\n"
        f"<code>> Mengesan signal XAU/USD...</code>\n\n"
        f"✨ <b>HADIAH PERCUMA DIKESAN!</b>\n"
        f"Sertai saluran kami sekarang untuk menebus hadiah eksklusif dan signal Gold premium."
    )
    
    # Inline button for the immediate redirect/gift
    inline_kb = [[InlineKeyboardButton("🎁 KLIK SINI UNTUK HADIAH PERCUMA", url=CHANNEL_URL)]]
    inline_markup = InlineKeyboardMarkup(inline_kb)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    
    await update.message.reply_text(
        "Sila sertai saluran rasmi kami di bawah untuk membuka akses penuh:",
        reply_markup=inline_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🚀 AKSES SIGNAL EMAS":
        # Premium Animation logic
        msg = await update.message.reply_text(f"{SYSTEM_LOG} <i>Menyambung ke pangkalan data signal...</i>", parse_mode="HTML")
        await asyncio.sleep(0.7)
        await msg.edit_text(f"{SYSTEM_LOG} <i>Menyinkronkan dengan KIRSH GOLD... [94%]</i>", parse_mode="HTML")
        await asyncio.sleep(0.7)
        
        final_text = (
            "🟢🟢🟢🟢🟢🟢🟢🟢\n\n"
            "<b>Sesi langsung kami akan bermula tidak lama lagi.</b>\n\n"
            "Ambil peluang untuk berdagang secara 100% percuma dan jana keuntungan bersama saya hari ini.\n\n"
            "👇 <b>SERTAI SALURAN DI SINI</b> 👇"
        )
        keyboard = [[InlineKeyboardButton("✅ MASUK SALURAN SEKARANG", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.edit_text(final_text, reply_markup=reply_markup, parse_mode="HTML")

    elif text == "📊 ANALISIS PASARAN":
        msg = await update.message.reply_text(f"🤖 <code>Menganalisis carta XAU/USD...</code>", parse_mode="HTML")
        await asyncio.sleep(1.2)
        
        analysis = (
            "🔍 <b>LAPORAN ANALISIS IA</b>\n"
            "————————————————————\n"
            "• <b>Aset:</b> GOLD (XAU/USD)\n"
            "• <b>Ketepatan Signal:</b> 93.8%\n"
            "• <b>Status:</b> Sedia untuk kemasukan (Entry)\n\n"
            "<code>[!] NOTA: Signal terperinci hanya dihantar di saluran Telegram rasmi.</code>"
        )
        keyboard = [[InlineKeyboardButton("📈 LIHAT SIGNAL LIVE", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.edit_text(analysis, reply_markup=reply_markup, parse_mode="HTML")

    elif text == "💎 JOIN VIP GRATIS":
        vip_text = (
            "🏆 <b>AKSES VIP PERCUMA</b>\n\n"
            "Kami sedang membuka slot terhad untuk ahli baru menyertai Group VIP tanpa sebarang kos.\n\n"
            "<b>Kelebihan VIP:</b>\n"
            "✅ Signal Gold Ketepatan Tinggi\n"
            "✅ Teknik Scalping Eksklusif\n"
            "✅ Pengurusan Risiko Profesional"
        )
        keyboard = [[InlineKeyboardButton("💎 TEBUS SLOT VIP ANDA", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(vip_text, reply_markup=reply_markup, parse_mode="HTML")

    elif text == "📞 HUBUNGI ADMIN":
        await update.message.reply_text(
            "👨‍💻 <b>PUSAT BANTUAN</b>\n\n"
            "Ada sebarang soalan tentang signal atau cara bermula? Sila hubungi team kami melalui saluran rasmi:\n\n"
            f"👉 {CHANNEL_URL}",
            parse_mode="HTML"
        )

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        print("CRITICAL: TOKEN MISSING")
        exit(1)
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("KIRSH GOLD Premium AI Agent is running...")
    application.run_polling()
