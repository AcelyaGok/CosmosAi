from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
from datetime import datetime
from ..database import save_user, save_birth_profile
from ..location_utils import resolve_city

# ConversationHandler'da kullanılacak state (adım) değerlerini tanımlıyoruz
# range(3) → (0,1,2) üretir
# Her biri konuşmanın bir aşamasını temsil eder
BIRTH_DATE, BIRTH_TIME, BIRTH_PLACE = range(3)

# /register komutu çalıştığında burası tetiklenir
# Kullanıcıdan ilk olarak doğum tarihi istenir
async def register_start(update, context):
    await update.message.reply_text(
        "Doğum tarihinizi girin (örn: 15.03.1998):"
    )
    # Sonraki adımın BIRTH_DATE olacağını söylüyoruz
    return BIRTH_DATE

async def get_birth_date(update, context):
    # Kullanıcının girdiği tarihi geçici olarak context içinde saklıyoruz
    # context.user_data → kullanıcıya özel veri tutar
    context.user_data["birth_date"] = update.message.text
    await update.message.reply_text(
        "Doğum saatinizi girin (örn: 14:30). Bilmiyorsanız 'bilmiyorum' yazın:"
    )
    return BIRTH_TIME

async def get_birth_time(update, context):
    text = update.message.text.strip()

    # "Bilmiyorum" özel durumu — saat opsiyonel
    if text.lower() in ["bilmiyorum", "bilmem", "yok"]:
        context.user_data["birth_time"] = None
        await update.message.reply_text(
            "Doğum yerinizi girin (örn: Istanbul, Turkey):"
        )
        return BIRTH_PLACE

    # HH:MM formatı validasyonu
    try:
        datetime.strptime(text, "%H:%M")
    except ValueError:
        await update.message.reply_text(
            "Saat formatı yanlış! Lütfen SS:DD formatında girin "
            "(örn: 14:30). Bilmiyorsanız 'bilmiyorum' yazın:"
        )
        return BIRTH_TIME  # aynı state'te kal, tekrar sor

    # Format doğruysa kaydet ve devam et
    context.user_data["birth_time"] = text
    await update.message.reply_text(
        "Doğum yerinizi girin (örn: Istanbul, Turkey):"
    )
    return BIRTH_PLACE

async def get_birth_place(update, context):
    city_text = update.message.text.strip()
    
    # Boş şehir kontrolü
    if not city_text:
        await update.message.reply_text(
            "Doğum yerinizi boş bırakamazsınız. Lütfen bir şehir girin (örn: Istanbul, Turkey):"
        )
        return BIRTH_PLACE
    
    user_id = update.effective_user.id
    
    # Tarih formatını dönüştür
    birth_date_str = context.user_data["birth_date"]
    try:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "Tarih formatı yanlış! Lütfen GG.AA.YYYY formatında girin (örn: 15.03.1998):"
        )
        return BIRTH_DATE
    
    # Kullanıcıya bekleme mesajı (geocoding 2-5 saniye sürebilir)
    await update.message.reply_text("🔍 Şehrinizi arıyorum, lütfen bekleyin...")
    
    # Geocoding: şehir → enlem/boylam/utc_offset
    try:
        location = resolve_city(city_text, birth_date)
    except ValueError as e:
        # Şehir bulunamadı veya tarih hatası
        await update.message.reply_text(
            f"❌ {str(e)}\n\nLütfen şehir adını tekrar girin (örn: Istanbul, Turkey):"
        )
        return BIRTH_PLACE
    except RuntimeError as e:
        # Geocoding servisine ulaşılamadı (internet sorunu vb.)
        await update.message.reply_text(
            "❌ Şu anda lokasyon servisi ile bağlantı kuramıyorum. "
            "Lütfen birkaç saniye sonra tekrar deneyin."
        )
        return BIRTH_PLACE
    
    # Geocoding başarılı — birth_data'yı dolu olarak hazırla
    birth_data = {
        "birth_info": {
            "date": birth_date,
            "time": context.user_data["birth_time"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "utc_offset": location["utc_offset"],
            "timezone": location["timezone"],
            "place_name": location["resolved_name"]
        }
    }
    
    # Veritabanına kaydetme
    save_user(user_id, update.effective_user.first_name)
    save_birth_profile(user_id, birth_data)
    
    # Kullanıcıya doğrulama mesajı
    await update.message.reply_text(
        f"✅ Bilgilerin kaydedildi!\n\n"
        f"📍 Konum: {location['resolved_name']}\n"
        f"🌍 Saat dilimi: {location['timezone']} (UTC{'+' if location['utc_offset'] >= 0 else ''}{location['utc_offset']})\n\n"
        f"Artık yorum alabilirsin."
    )
    return ConversationHandler.END
    
    #Kaydedilecek veriyi hazırlama
    birth_data = {
        "birth_info": {
            "date": birth_date,
            "time": context.user_data["birth_time"],
            "latitude": None,
            "longitude": None
        }
    }


    # Veritabanına kaydetme
    save_user(user_id, update.effective_user.first_name)
    save_birth_profile(user_id, birth_data)

    await update.message.reply_text("✅ Bilgilerin kaydedildi! Artık yorum alabilirsin.")
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Kayıt iptal edildi.")
    return ConversationHandler.END

# Conversation Handler tanımı
register_handler = ConversationHandler(
    # Konusmayı baslatan komut
    entry_points=[CommandHandler("register", register_start)],
    # Her state için hangi fonksiyon çalışacak
    states={
        BIRTH_DATE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_date)],
        BIRTH_TIME:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_time)],
        BIRTH_PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_birth_place)],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)



