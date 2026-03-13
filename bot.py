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
SYSTEM_LOG = "<code>[AI SYSTEM]:</code>"

# --- Bot Logic ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium Welcome in English with AI Terminal feel."""
    user_name = update.effective_user.first_name
    
    # Premium Menu Layout
    keyboard = [
        ["🚀 ACCESS GOLD SIGNALS"],
        ["📊 MARKET ANALYSIS", "💎 JOIN FREE VIP"],
        ["📞 CONTACT ADMIN"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        f"🤖 <b>KIRSH GOLD AI TERMINAL</b>\n"
        f"————————————————————\n"
        f"Welcome, <b>{user_name}</b>. System encryption active.\n\n"
        f"<code>> Scanning market liquidity...</code>\n"
        f"<code>> Detecting XAU/USD signals...</code>\n\n"
        f"✨ <b>FREE GIFT DETECTED!</b>\n"
        f"Join our channel now to redeem your exclusive gift and premium Gold signals."
    )
    
    # Inline button for the immediate redirect/gift
    inline_kb = [[InlineKeyboardButton("🎁 CLICK HERE FOR FREE GIFT", url=CHANNEL_URL)]]
    inline_markup = InlineKeyboardMarkup(inline_kb)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    
    await update.message.reply_text(
        "Please join our official channel below to unlock full access:",
        reply_markup=inline_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🚀 ACCESS GOLD SIGNALS":
        # Premium Animation logic
        msg = await update.message.reply_text(f"{SYSTEM_LOG} <i>Connecting to signal database...</i>", parse_mode="HTML")
        await asyncio.sleep(0.7)
        await msg.edit_text(f"{SYSTEM_LOG} <i>Syncing with KIRSH GOLD... [94%]</i>", parse_mode="HTML")
        await asyncio.sleep(0.7)
        
        final_text = (
            "🟢🟢🟢🟢🟢🟢🟢🟢\n\n"
            "<b>Our live session will start soon.</b>\n\n"
            "Take the opportunity to trade 100% for free and generate profits with me today.\n\n"
            "👇 <b>JOIN CHANNEL HERE</b> 👇"
        )
        keyboard = [[InlineKeyboardButton("✅ ENTER CHANNEL NOW", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.edit_text(final_text, reply_markup=reply_markup, parse_mode="HTML")

    elif text == "📊 MARKET ANALYSIS":
        msg = await update.message.reply_text(f"🤖 <code>Analyzing XAU/USD charts...</code>", parse_mode="HTML")
        await asyncio.sleep(1.2)
        
        analysis = (
            "🔍 <b>AI ANALYSIS REPORT</b>\n"
            "————————————————————\n"
            "• <b>Asset:</b> GOLD (XAU/USD)\n"
            "• <b>Signal Accuracy:</b> 93.8%\n"
            "• <b>Status:</b> Ready for Entry\n\n"
            "<code>[!] NOTE: Detailed signals are sent exclusively in the official Telegram channel.</code>"
        )
        keyboard = [[InlineKeyboardButton("📈 VIEW LIVE SIGNALS", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await msg.edit_text(analysis, reply_markup=reply_markup, parse_mode="HTML")

    elif text == "💎 JOIN FREE VIP":
        vip_text = (
            "🏆 <b>FREE VIP ACCESS</b>\n\n"
            "We are currently opening limited slots for new members to join the VIP Group at no cost.\n\n"
            "<b>VIP Benefits:</b>\n"
            "✅ High Accuracy Gold Signals\n"
            "✅ Exclusive Scalping Techniques\n"
            "✅ Professional Risk Management"
        )
        keyboard = [[InlineKeyboardButton("💎 REDEEM YOUR VIP SLOT", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(vip_text, reply_markup=reply_markup, parse_mode="HTML")

    elif text == "📞 CONTACT ADMIN":
        await update.message.reply_text(
            "👨‍💻 <b>HELP CENTER</b>\n\n"
            "Have any questions about signals or how to get started? Please contact our team through the official channel:\n\n"
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
