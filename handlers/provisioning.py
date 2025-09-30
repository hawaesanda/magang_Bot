import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

# Command handlers (existing)
async def funneling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /funneling"""
    logger.info("📈 Funneling command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_FUNNELING, 
        "funneling.png", 
        config.CROP_DEFAULT, 
        "📈 Funneling",
        "📈 Memuat Funneling...\nMohon tunggu sebentar..."
    )

async def detail_kendala_psb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /detail_kendala_psb"""
    logger.info("🔍 Detail Kendala PSB command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_KENDALA_PSB, 
        "detail_kendala_psb.png", 
        config.CROP_DEFAULT, 
        "🔍 Detail Kendala PSB",
        "🔍 Memuat Detail Kendala PSB...\nMohon tunggu sebentar..."
    )

async def detail_wo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /detail_wo"""
    logger.info("📋 Detail WO command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_WO, 
        "detail_wo.png", 
        config.CROP_DEFAULT, 
        "📋 Detail WO",
        "📋 Memuat Detail WO...\nMohon tunggu sebentar..."
    )

# Callback handlers for menu buttons
async def funneling_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Funneling di menu"""
    logger.info("📈 Funneling callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_FUNNELING,
        filename="funneling.png",
        crop_config=config.CROP_DEFAULT,
        caption="📈 Funneling",
        loading_text="📈 Memuat Funneling...\nMohon tunggu sebentar...",
        back_menu="menu_provisioning"
    )

async def detail_kendala_psb_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Detail Kendala PSB di menu"""
    logger.info("🔍 Detail Kendala PSB callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_DETAIL_KENDALA_PSB,
        filename="detail_kendala_psb.png",
        crop_config=config.CROP_DEFAULT,
        caption="🔍 Detail Kendala PSB",
        loading_text="🔍 Memuat Detail Kendala PSB...\nMohon tunggu sebentar...",
        back_menu="menu_provisioning"
    )

async def detail_wo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Detail WO di menu"""
    logger.info("📋 Detail WO callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_DETAIL_WO,
        filename="detail_wo.png",
        crop_config=config.CROP_DEFAULT,
        caption="📋 Detail WO",
        loading_text="📋 Memuat Detail WO...\nMohon tunggu sebentar...",
        back_menu="menu_provisioning"
    )
