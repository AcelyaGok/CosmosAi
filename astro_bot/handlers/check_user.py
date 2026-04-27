from telegram.ext import CommandHandler
import sys
import os
# projedeki farklı klasörlerden dosya import edebilmek icin mevcut dosyanın bulunduğu klasörün bir üst dizinini Python path'ine ekler


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# InlineKeyboardButton → tek bir butonu temsil eder.
# InlineKeyboardMarkup → butonları bir araya getirip mesaja eklenebilir hale getirir.
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# get_user → kullanıcıyı veritabanından çeker
from database import get_user

# bu fonksiyon sayesinde bot birden fazla kullanıcıya yanit verebilir
async def check_user(update, context):
    # kullanıcının benzersiz id'si 
    user_id = update.effective_user.id
    # kullanıcı veritabanında var mı kontrol ediyoruz
    user = get_user(user_id)
    print(f"Kullanıcı: {user_id}, DB'de var mı: {user}")
    if user:
        # Butonların alt alta dizilmesini saglar.
        # callback_data → kullanıcı butona tıkladığında arka planda gelen gizli veridir.
        keyboard = [
            [InlineKeyboardButton("🔮 Günlük Yorum", callback_data="gunluk")],
            [InlineKeyboardButton("📅 Haftalık Yorum", callback_data="haftalik")],
            [InlineKeyboardButton("🗺️ Doğum Haritam", callback_data="dogum_haritam")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        #reply_text() → mesajı gönderir
        #reply_markup → mesajın altına butonları ekler
        await update.message.reply_text(
            "Tekrar hoş geldin! Ne yapmak istersin?",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Seni tanımıyorum! Önce kayıt olman gerekiyor.\n"
            "/register yazarak başlayabilirsin."
        )
    
    
