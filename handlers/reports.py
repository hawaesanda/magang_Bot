import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

# Command handler for MSA/WSA
async def msawsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_screenshot_command(
        update, context,
        config.LOOKER_STUDIO_MSA_WSA_URL,
        "msawsa.png",
        config.CROP_MSAWSA,
        "📊 Laporan MSA/WSA"
    )

# Command handler for Pilaten
async def pilaten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_screenshot_command(
        update, context,
        config.LOOKER_STUDIO_PILATEN_URL,
        "pilaten.png",
        config.CROP_PILATEN,
        "📊 Laporan PI LATEN"
    )
