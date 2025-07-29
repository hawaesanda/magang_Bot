import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def monitoring_ticket_b2b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏬 Monitoring Ticket B2B command dipanggil")
    await update.message.reply_text("Memuat Laporan Monitoring Ticket B2B.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MONITORING_TICKET_B2B, "monitoring_ticket_b2b.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="🏬 Laporan Monitoring Ticket B2B")
            os.remove(path)
            logger.info("🏬 Monitoring Ticket B2B command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket B2B.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🏬 Error di Monitoring Ticket B2B handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket B2B.\nMohon coba lagi.")

async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📊 Performance command dipanggil")
    await update.message.reply_text("Memuat Laporan Performance.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PERFORMANCE, "performance.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📊 Laporan Performance")
            os.remove(path)
            logger.info("📊 Performance command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Performance.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📊 Error di Performance handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Performance.\nMohon coba lagi.")
