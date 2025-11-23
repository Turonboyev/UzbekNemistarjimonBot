from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from googletrans import Translator

TOKEN = "7850816062:AAEx9dIMfxYZi0Xm6mHDlOaJiZHyv1udDyY"
ADMIN_BOT_LINK = "@BotAdmins19s_bot"

translator = Translator()

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🇺🇿 O‘zbek → 🇩🇪 Nemis", callback_data="uzde")],
        [InlineKeyboardButton("🇩🇪 Nemis → 🇺🇿 O‘zbek", callback_data="deuz")],
        [InlineKeyboardButton("⚙ Admin panel", callback_data="admin")]
    ]
    update.message.reply_text(
        "Tarjimon botga xush kelibsiz!\nTilni tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button(update: Update, context: CallbackContext):
    q = update.callback_query
    q.answer()

    # Tilni tanlash
    if q.data == "uzde":
        context.user_data["lang"] = "uzde"
        q.edit_message_text("O‘zbek tilidagi matnni yuboring, nemis tiliga tarjima qilaman.")

    elif q.data == "deuz":
        context.user_data["lang"] = "deuz"
        q.edit_message_text("Nemis tilidagi matnni yuboring, o‘zbek tiliga tarjima qilaman.")

    elif q.data == "admin":
        q.edit_message_text(
            f"Admin panelga kirish uchun ushbu botga start bosing:\n{ADMIN_BOT_LINK}"
        )

def translate(update: Update, context: CallbackContext):
    text = update.message.text
    lang = context.user_data.get("lang")

    if not lang:
        update.message.reply_text("Avval tilni tanlang: /start")
        return

    if lang == "uzde":
        translated = translator.translate(text, src="uz", dest="de").text
    else:
        translated = translator.translate(text, src="de", dest="uz").text

    update.message.reply_text(translated)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
