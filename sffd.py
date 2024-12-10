from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random

# Персонаж игрока
player = {
    "name": "",
    "class": "",
    "hp": 100,
    "attack": 10,
    "gold": 0,
    "level": 1
}

# События
events = [
    "Вы нашли сундук с золотом! +10 золота.",
    "На вас напал гоблин! Вы сражаетесь.",
    "Вы наткнулись на ловушку! -10 HP.",
    "Вы нашли лечебное зелье! +20 HP."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Воин", "Маг", "Вор"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в 'Хроники Авантюриста'! Выберите свой класс:", reply_markup=reply_markup
    )

async def choose_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player["class"] = update.message.text
    await update.message.reply_text(f"Вы выбрали класс: {player['class']}. Теперь отправляйтесь в приключение!")
    await adventure(update, context)

async def adventure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event = random.choice(events)
    if "гоблин" in event:
        await fight(update, context)
    elif "сундук" in event:
        player["gold"] += 10
    elif "ловушка" in event:
        player["hp"] -= 10
    elif "зелье" in event:
        player["hp"] += 20
    await update.message.reply_text(event)

async def fight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("На вас напал враг! Битва начинается!")

def main():
    app = Application.builder().token("7569869866:AAE0-Srm8IxOIO6qH10nWMCzMfJ1GQP6GXg").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_class))

    app.run_polling()

if __name__ == "__main__":
    main()