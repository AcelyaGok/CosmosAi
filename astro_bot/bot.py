from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN
from handlers.registration import register_handler
from handlers.check_user import check_user

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", check_user))
    app.add_handler(register_handler)
    
    print("Bot çalışıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()