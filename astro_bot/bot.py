from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN
from handlers.registration import register_handler #register handler import edildi

async def start(update : Update , context : ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

    "Merhaba! Ben astroloji botuyum \n"
    "Sana kişisel yorum yapabilmem için birkaç bilgiye ihtiyacım var.\n\n"
    "Doğum tarihinizi girin (örnek: 1998-05-12):"

    )

def main():
    app=ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start" ,start))
    print("Bot çalışıyor…")
    app.add_handler(register_handler) #botu handlera baglar
    app.run_polling()

if __name__ == "__main__":
    main()