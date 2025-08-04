import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

async def funneling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔄 Funneling command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_FUNNELING, 
        "funneling.png", 
        config.CROP_DEFAULT, 
        "🔄 Laporan Funneling"
    )

async def detail_kendala_psb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔧 Detail Kendala PSB command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_KENDALA_PSB, 
        "detail_kendala_psb.png", 
        config.CROP_DEFAULT, 
        "🔧 Laporan Detail Kendala PSB"
    )

async def detail_wo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📝 Detail WO command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_WO, 
        "detail_wo.png", 
        config.CROP_DEFAULT, 
        "📝 Laporan Detail WO"
    )
