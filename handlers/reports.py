import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

# Command handler for MSA/WSA
async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan MSA/WSA.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_MSA_WSA_URL,
        filename="msawsa.png",
        crop_box=config.CROP_MSAWSA,
        caption="📊 Laporan MSA/WSA"
    )

# Command handler for Pilaten
async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan PI LATEN.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_PILATEN_URL,
        filename="pilaten.png",
        crop_box=config.CROP_PILATEN,
        caption="📊 Laporan PI LATEN"
    )
