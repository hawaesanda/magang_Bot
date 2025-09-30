import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /msawsa"""
    logger.info("📊 MSA/WSA command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MSA_WSA_URL, 
        "msawsa.png", 
        config.CROP_MSAWSA, 
        "📊 Laporan MSA/WSA",
        "📊 Memuat laporan MSA/WSA...\nMohon tunggu sebentar..."
    )

async def msawsa_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol MSA/WSA di menu"""
    logger.info("📊 MSA/WSA callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_MSA_WSA_URL,
        filename="msawsa.png",
        crop_config=config.CROP_MSAWSA,
        caption="📊 Laporan MSA/WSA",
        loading_text="📊 Memuat laporan MSA/WSA...\nMohon tunggu sebentar...",
        back_menu="main_menu"
    )
