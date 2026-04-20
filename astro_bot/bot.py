from Telegram import update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN

async def start(update : update , context : ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

    "Merhaba! Ben astroloji botuyum \n"
    "Sana kişisel yorum yapabilmem için birkaç bilgiye ihtiyacım var.\n\n"
    "Doğum tarihinizi girin (örnek: 1998-05-12):"

    )

def main():
    app=ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start" ,start))
    print("Bot çalışıyor…")
    app.run_polling()

if __name__ == "__main__":
    main()