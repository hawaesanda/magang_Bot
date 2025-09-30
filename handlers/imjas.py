import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

async def imjas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /imjas"""
    logger.info("📱 IMJAS command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_IMJAS, 
        "imjas.png", 
        config.CROP_DEFAULT, 
        "📱 Dashboard IMJAS"
    )

async def imjas_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol IMJAS di menu"""
    logger.info("📱 IMJAS callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_IMJAS,
        filename="imjas.png",
        crop_config=config.CROP_DEFAULT,
        caption="📱 Dashboard IMJAS",
        loading_text="📱 Memuat IMJAS Dashboard...\nMohon tunggu sebentar...",
        back_menu="main_menu"
    )
