from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

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
    
    # Kişi 3'ün fonksiyonlarını çağır
    save_user(user_id, update.effective_user.first_name)
    save_birth_profile(
        telegram_user_id=user_id,
        birth_date=context.user_data["birth_date"],
        birth_time=context.user_data["birth_time"],
        birth_place_text=context.user_data["birth_place"]
    )
    
    await update.message.reply_text("✅ Bilgilerin kaydedildi! Artık yorum alabilirsin.")
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Kayıt iptal edildi.")
    return ConversationHandler.END

from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", register_start)],
    states={
        BIRTH_DATE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_date)],
        BIRTH_TIME:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_time)],
        BIRTH_PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_place)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

