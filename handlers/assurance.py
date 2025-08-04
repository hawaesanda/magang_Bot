import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils

logger = logging.getLogger(__name__)

# Command handler for monitoring ticket
async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔧 Monitoring command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Monitoring Ticket.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_MONITORING,
        filename="monitoring.png",
        crop_box=config.CROP_MONITORING,
        caption="📊 Laporan Monitoring"
    )
    
    if success:
        logger.info("🔧 Monitoring command selesai")
    else:
        logger.error("🔧 Monitoring command gagal")

async def closed_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📋 Closed Ticket command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan Closed Ticket.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_CLOSED_TICKET,
        filename="closed_ticket.png",
        crop_box=config.CROP_DEFAULT,
        caption="📋 Laporan Closed Ticket"
    )
    
    if success:
        logger.info("📋 Closed Ticket command selesai")
    else:
        logger.error("📋 Closed Ticket command gagal")

async def unspec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("⚠️ UNSPEC command dipanggil")
    
    success = await utils.send_report_with_loading_cleanup(
        update=update,
        context=context,
        loading_message="Memuat Laporan UNSPEC.\nMohon Tunggu Sebentar...",
        screenshot_url=config.LOOKER_STUDIO_UNSPEC,
        filename="unspec.png",
        crop_box=config.CROP_DEFAULT,
        caption="⚠️ Laporan UNSPEC"
    )
    
    if success:
        logger.info("⚠️ UNSPEC command selesai")
    else:
        logger.error("⚠️ UNSPEC command gagal")
