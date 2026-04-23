from telegram.ext import CommandHandler
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_user, save_user, save_birth_profile

async def check_user(update, context):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if user:
        # Kayıtlı kullanıcı → direkt menüye yönlendir
        await update.message.reply_text(
            f"Tekrar hoş geldin! Ne yapmak istersin?"
        )
    else:
        # Yeni kullanıcı → kayıt akışına yönlendir
        await update.message.reply_text(
            "Seni tanımıyorum! Önce kayıt olman gerekiyor.\n"
            "/register yazarak başlayabilirsin."
        )