import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

# Command handlers (existing)
async def funneling_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /funneling_indbiz"""
    logger.info("📈 Funneling INDBIZ command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_FUNNELING_INDBIZ, 
        "funneling_indbiz.png", 
        config.CROP_DEFAULT, 
        "📈 Funneling INDBIZ",
        "📈 Memuat Funneling INDBIZ...\nMohon tunggu sebentar..."
    )

async def detail_kendala_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /detail_kendala_indbiz"""
    logger.info("🔍 Detail Kendala INDBIZ command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ, 
        "detail_kendala_indbiz.png", 
        config.CROP_DEFAULT, 
        "🔍 Detail Kendala INDBIZ",
        "🔍 Memuat Detail Kendala INDBIZ...\nMohon tunggu sebentar..."
    )

async def detail_wo_indbiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /detail_wo_indbiz"""
    logger.info("📋 Detail WO INDBIZ command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_DETAIL_WO_INDBIZ, 
        "detail_wo_indbiz.png", 
        config.CROP_DEFAULT, 
        "📋 Detail WO INDBIZ",
        "📋 Memuat Detail WO INDBIZ...\nMohon tunggu sebentar..."
    )

# Callback handlers for menu buttons
async def funneling_indbiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Funneling INDBIZ di menu"""
    logger.info("📈 Funneling INDBIZ callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_FUNNELING_INDBIZ,
        filename="funneling_indbiz.png",
        crop_config=config.CROP_DEFAULT,
        caption="📈 Funneling INDBIZ",
        loading_text="📈 Memuat Funneling INDBIZ...\nMohon tunggu sebentar...",
        back_menu="menu_indbiz"
    )

async def detail_kendala_indbiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Detail Kendala INDBIZ di menu"""
    logger.info("🔍 Detail Kendala INDBIZ callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_DETAIL_KENDALA_INDBIZ,
        filename="detail_kendala_indbiz.png",
        crop_config=config.CROP_DEFAULT,
        caption="🔍 Detail Kendala INDBIZ",
        loading_text="🔍 Memuat Detail Kendala INDBIZ...\nMohon tunggu sebentar...",
        back_menu="menu_indbiz"
    )

async def detail_wo_indbiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Detail WO INDBIZ di menu"""
    logger.info("📋 Detail WO INDBIZ callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_DETAIL_WO_INDBIZ,
        filename="detail_wo_indbiz.png",
        crop_config=config.CROP_DEFAULT,
        caption="📋 Detail WO INDBIZ",
        loading_text="📋 Memuat Detail WO INDBIZ...\nMohon tunggu sebentar...",
        back_menu="menu_indbiz"
    )
