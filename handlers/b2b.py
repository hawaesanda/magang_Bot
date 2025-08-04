import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

async def monitoring_ticket_b2b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏬 Monitoring Ticket B2B command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING_TICKET_B2B, 
        "monitoring_ticket_b2b.png", 
        config.CROP_DEFAULT, 
        "🏬 Laporan Monitoring Ticket B2B"
    )

async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📊 Performance command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_PERFORMANCE, 
        "performance.png", 
        config.CROP_DEFAULT, 
        "📊 Laporan Performance"
    )
