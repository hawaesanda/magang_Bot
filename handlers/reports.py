import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

# Command handler for MSA/WSA
async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Memuat Laporan MSA/WSA.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_MSA_WSA_URL, "msawsa.png", config.CROP_MSAWSA)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="📊 Laporan MSA/WSA")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal menampilkan laporan MSA/WSA.\nMohon coba lagi.")

# Command handler for Pilaten
async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Memuat Laporan PI LATEN.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    path = await utils.get_looker_studio_screenshot(config.LOOKER_STUDIO_PILATEN_URL, "pilaten.png", config.CROP_PILATEN)
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            await update.message.reply_photo(f, caption="📊 Laporan PI LATEN")
        os.remove(path)
    else:
        await update.message.reply_text("❌ Gagal menampilkan laporan PI LATEN.\nMohon coba lagi.")
