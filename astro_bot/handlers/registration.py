from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import save_user, save_birth_profile

BIRTH_DATE, BIRTH_TIME, BIRTH_PLACE = range(3)

async def register_start(update, context):
    await update.message.reply_text(
        "Doğum tarihinizi girin (örn: 15.03.1998):"
    )
    return BIRTH_DATE

async def get_birth_date(update, context):
    context.user_data["birth_date"] = update.message.text
    await update.message.reply_text(
        "Doğum saatinizi girin (örn: 14:30). Bilmiyorsanız 'bilmiyorum' yazın:"
    )
    return BIRTH_TIME

async def get_birth_time(update, context):
    text = update.message.text
    context.user_data["birth_time"] = None if "bilmiyorum" in text.lower() else text
    await update.message.reply_text(
        "Doğum yerinizi girin (örn: Istanbul, Turkey):"
    )
    return BIRTH_PLACE

async def get_birth_place(update, context):
    context.user_data["birth_place"] = update.message.text
    user_id = update.effective_user.id

    # Tarih formatını DD.MM.YYYY'den YYYY-MM-DD'ye çevir
    birth_date_str = context.user_data["birth_date"]
    try:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "Tarih formatı yanlış! Lütfen GG.AA.YYYY formatında girin (örn: 15.03.1998):"
        )
        return BIRTH_DATE

    birth_data = {
        "birth_info": {
            "date": birth_date,
            "time": context.user_data["birth_time"],
            "latitude": None,
            "longitude": None
        }
    }

    save_user(user_id, update.effective_user.first_name)
    save_birth_profile(user_id, birth_data)

    await update.message.reply_text("✅ Bilgilerin kaydedildi! Artık yorum alabilirsin.")
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Kayıt iptal edildi.")
    return ConversationHandler.END

register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register_start)],
    states={
        BIRTH_DATE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_date)],
        BIRTH_TIME:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_time)],
        BIRTH_PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_place)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)



