import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

async def monitoring_ticket_b2b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🏬 Monitoring Ticket B2B command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Monitoring Ticket B2B.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_MONITORING_TICKET_B2B,
        filename="monitoring_ticket_b2b.png",
        crop_box=config.CROP_DEFAULT,
        caption="🏬 Laporan Monitoring Ticket B2B"
    )
    
    if success:
        logger.info("🏬 Monitoring Ticket B2B command selesai")
    else:
        logger.error("🏬 Monitoring Ticket B2B command gagal")

async def performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📊 Performance command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Performance.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_PERFORMANCE,
        filename="performance.png",
        crop_box=config.CROP_DEFAULT,
        caption="📊 Laporan Performance"
    )
    
    if success:
        logger.info("📊 Performance command selesai")
    else:
        logger.error("📊 Performance command gagal")
