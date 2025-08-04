import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

async def funneling_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Funneling INDBIZ command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_FUNNELING_INDBIZ, 
        "funneling_indbiz.png", 
        config.CROP_DEFAULT, 
        "🏢 Laporan Funneling INDBIZ"
    )

async def detail_kendala_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Detail Kendala INDBIZ command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ, 
        "detail_kendala_indbiz.png", 
        config.CROP_DEFAULT, 
        "🏢 Laporan Detail Kendala INDBIZ"
    )

async def detail_wo_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏢 Detail WO INDBIZ command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_WO_INDBIZ, 
        "detail_wo_indbiz.png", 
        config.CROP_DEFAULT, 
        "🏢 Laporan Detail WO INDBIZ"
    )
