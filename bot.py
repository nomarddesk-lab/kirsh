import os
import threading
import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- Web Server for Render.com ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Gari Bot is active!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Bot Content (English Learning Material) ---

LEARNING_CONTENT = [
    # Day 1: Introduction & The "Gari" Concept
    "The name of our channel 'Gari' reflects our goal of being close to you, just like a neighbor who helps another. We don't just deliver information; we walk with you on the 'Learning in Progress' (Gari) journey toward mastery.\n\nWhat sets us apart?\n- Conversation focus: We focus on the English you actually use in daily life.\n- Live classes: Interactive sessions to answer questions and correct pronunciation.\n- Support community: A club where everyone helps each other.\n\nWelcome Gift: Live classes will be free for the first 1,000 subscribers!",
    
    # Day 2: Why English in 2026?
    "Why is English the key to your success in 2026?\n\nIn today's world, English is no longer a bonus; it is a basic necessity for personal and professional growth. It is the language of science, business, and global communication.\n\nMany study for years without results due to a lack of real interaction. The Gari channel changes this reality with an environment focused on practical application instead of just theory.\n\nFree opportunity for the first 1,000 subscribers to the channel!",
    
    # Day 3: Apps vs. Real Practice
    "Why are language apps alone not enough for fluency?\n\nDo you ever feel like you understand the grammar in the app but freeze when it's time to speak? The reason is simple: language is a social practice. Apps give information, but they don't give the confidence of a real conversation.\n\nGari Vision:\n- Immediate correction: In the lives, we correct your mistakes on the spot.\n- Simplified information: We explain English in a direct way.\n- Interactive environment: Group learning eliminates shyness.\n\nLimited spots for the first 1,000!"
]

QUIZ_DATA = [
    {
        "question": "What is the primary goal of the name 'Gari'?",
        "options": ["To be close and help like a neighbor", "To sell electronics", "A delivery service"],
        "correct": 0
    },
    {
        "question": "What is missing in traditional apps according to Gari?",
        "options": ["Pretty colors", "Social practice and confidence", "Too many words"],
        "correct": 1
    },
    {
        "question": "Who has access to the free live classes?",
        "options": ["Everyone forever", "No one", "The first 1,000 subscribers"],
        "correct": 2
    }
]

# --- Bot Logic ---
user_progress = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"day": 0, "quiz_day": 0, "last_learned_date": None}
    
    # Menu in English
    keyboard = [
        ["Start Learning 📖", "Today's Quiz 🧠"],
        ["Pause for Today ✋"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        "Welcome to the Gari Learning Bot! 🏠\n\n"
        "We are here to walk with you step-by-step toward fluency.\n"
        "Choose an option from the menu below to get started."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if user_id not in user_progress:
        user_progress[user_id] = {"day": 0, "quiz_day": 0, "last_learned_date": None}

    if text == "Start Learning 📖":
        current_day = user_progress[user_id]["day"]
        today = str(datetime.now().date())
        
        if user_progress[user_id]["last_learned_date"] == today:
            await update.message.reply_text("You have already finished today's lesson! Come back tomorrow for more. ✨")
            return

        if current_day < len(LEARNING_CONTENT):
            await update.message.reply_text(LEARNING_CONTENT[current_day])
            user_progress[user_id]["day"] += 1
            user_progress[user_id]["last_learned_date"] = today
        else:
            await update.message.reply_text("You have finished all available lessons! Stay tuned for updates.")

    elif text == "Today's Quiz 🧠":
        current_quiz_idx = user_progress[user_id]["quiz_day"]
        
        if current_quiz_idx < len(QUIZ_DATA):
            q = QUIZ_DATA[current_quiz_idx]
            buttons = [[InlineKeyboardButton(opt, callback_data=f"quiz_{idx}")] for idx, opt in enumerate(q["options"])]
            reply_markup = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(f"Quiz Question:\n\n{q['question']}", reply_markup=reply_markup)
        else:
            await update.message.reply_text("You have completed all available quizzes! Great job.")

    elif text == "Pause for Today ✋":
        await update.message.reply_text("Take a rest! We'll be waiting for you tomorrow to continue the journey. ☕")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    current_quiz_idx = user_progress[user_id]["quiz_day"]
    if current_quiz_idx >= len(QUIZ_DATA):
        return

    selected_option = int(query.data.split("_")[1])
    if selected_option == QUIZ_DATA[current_quiz_idx]["correct"]:
        feedback = "Correct answer! ✅\n\n"
    else:
        feedback = "Good try! But that wasn't it.\n\n"
    
    feedback += "Your learning is progressing very well, come back tomorrow for a new question! 🌟"
    user_progress[user_id]["quiz_day"] += 1
    await query.edit_message_text(text=feedback)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        print("CRITICAL ERROR: TELEGRAM_TOKEN environment variable is missing.")
        exit(1)
    
    print("Starting Gari Bot (English Version)...")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    application.run_polling()
