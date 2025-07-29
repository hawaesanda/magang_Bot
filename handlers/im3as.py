import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def im3as(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📱 IM3AS command dipanggil")
    await update.message.reply_text("Memuat Dashboard IM3AS.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_IM3AS, "im3as.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📱 Dashboard IM3AS")
            os.remove(path)
            logger.info("📱 IM3AS command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan Dashboard IM3AS.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📱 Error di IM3AS handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan Dashboard IM3AS.\nMohon coba lagi.")
