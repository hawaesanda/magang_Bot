import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

async def imjas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📱 IMJAS command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_IMJAS, 
        "imjas.png", 
        config.CROP_DEFAULT, 
        "📱 Dashboard IMJAS"
    )
