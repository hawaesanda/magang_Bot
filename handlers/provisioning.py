import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def funneling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔄 Funneling command dipanggil")
    await update.message.reply_text("Memuat Laporan Funneling.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_FUNNELING, "funneling.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="🔄 Laporan Funneling")
            os.remove(path)
            logger.info("🔄 Funneling command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Funneling.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🔄 Error di Funneling handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Funneling.\nMohon coba lagi.")

async def detail_kendala_psb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔧 Detail Kendala PSB command dipanggil")
    await update.message.reply_text("Memuat Laporan Detail Kendala PSB.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_KENDALA_PSB, "detail_kendala_psb.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="🔧 Laporan Detail Kendala PSB")
            os.remove(path)
            logger.info("🔧 Detail Kendala PSB command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala PSB.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🔧 Error di Detail Kendala PSB handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala PSB.\nMohon coba lagi.")

async def detail_wo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📝 Detail WO command dipanggil")
    await update.message.reply_text("Memuat Laporan Detail WO.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_WO, "detail_wo.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📝 Laporan Detail WO")
            os.remove(path)
            logger.info("📝 Detail WO command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📝 Error di Detail WO handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO.\nMohon coba lagi.")
