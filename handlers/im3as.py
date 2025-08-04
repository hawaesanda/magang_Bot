import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def im3as(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📱 IM3AS command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Dashboard IM3AS.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_IM3AS,
        filename="im3as.png",
        crop_box=config.CROP_DEFAULT,
        caption="📱 Dashboard IM3AS"
    )
    
    if success:
        logger.info("📱 IM3AS command selesai")
    else:
        logger.error("📱 IM3AS command gagal")
