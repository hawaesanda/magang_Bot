import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

async def im3as(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📱 IM3AS command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_IM3AS, 
        "im3as.png", 
        config.CROP_DEFAULT, 
        "📱 Dashboard IM3AS"
    )
