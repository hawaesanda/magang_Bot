import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

# Command handlers (existing)
async def monitoring_ticket_b2b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /monitoring_ticket_b2b"""
    logger.info("📊 Monitoring Ticket B2B command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING_TICKET_B2B, 
        "monitoring_ticket_b2b.png", 
        config.CROP_DEFAULT, 
        "📊 Monitoring Ticket B2B",
        "📊 Memuat Monitoring Ticket B2B...\nMohon tunggu sebentar..."
    )

async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /performance"""
    logger.info("📈 Performance command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_PERFORMANCE, 
        "performance.png", 
        config.CROP_DEFAULT, 
        "📈 Performance",
        "📈 Memuat Performance...\nMohon tunggu sebentar..."
    )

# Callback handlers for menu buttons
async def monitoring_ticket_b2b_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Monitoring Ticket B2B di menu"""
    logger.info("📊 Monitoring Ticket B2B callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_MONITORING_TICKET_B2B,
        filename="monitoring_ticket_b2b.png",
        crop_config=config.CROP_DEFAULT,
        caption="📊 Monitoring Ticket B2B",
        loading_text="📊 Memuat Monitoring Ticket B2B...\nMohon tunggu sebentar...",
        back_menu="menu_b2b"
    )

async def performance_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Performance di menu"""
    logger.info("📈 Performance callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_PERFORMANCE,
        filename="performance.png",
        crop_config=config.CROP_DEFAULT,
        caption="📈 Performance",
        loading_text="📈 Memuat Performance...\nMohon tunggu sebentar...",
        back_menu="menu_b2b"
    )
