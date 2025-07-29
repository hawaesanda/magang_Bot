import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def funneling_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Funneling INDBIZ command dipanggil")
    await update.message.reply_text("Memuat Laporan Funneling INDBIZ.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_FUNNELING_INDBIZ, "funneling_indbiz.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="🏢 Laporan Funneling INDBIZ")
            os.remove(path)
            logger.info("🏢 Funneling INDBIZ command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Funneling INDBIZ.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🏢 Error di Funneling INDBIZ handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Funneling INDBIZ.\nMohon coba lagi.")

async def detail_kendala_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Detail Kendala INDBIZ command dipanggil")
    await update.message.reply_text("Memuat Laporan Detail Kendala INDBIZ.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ, "detail_kendala_indbiz.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="🏢 Laporan Detail Kendala INDBIZ")
            os.remove(path)
            logger.info("🏢 Detail Kendala INDBIZ command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala INDBIZ.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🏢 Error di Detail Kendala INDBIZ handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Detail Kendala INDBIZ.\nMohon coba lagi.")

async def detail_wo_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Detail WO INDBIZ command dipanggil")
    await update.message.reply_text("Memuat Laporan Detail WO INDBIZ.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_DETAIL_WO_INDBIZ, "detail_wo_indbiz.png", config.CROP_DEFAULT)
        
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="🏢 Laporan Detail WO INDBIZ")
            os.remove(path)
            logger.info("🏢 Detail WO INDBIZ command selesai")
        else:
            await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO INDBIZ.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🏢 Error di Detail WO INDBIZ handler: {e}")
        await update.message.reply_text("❌ Gagal menampilkan laporan Detail WO INDBIZ.\nMohon coba lagi.")
