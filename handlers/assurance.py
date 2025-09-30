import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

# Command handlers (existing)
async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /monitoring_ticket"""
    logger.info("📊 Monitoring Ticket command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "monitoring.png", 
        config.CROP_MONITORING, 
        "📊 Monitoring Ticket",
        "📊 Memuat Monitoring Ticket...\nMohon tunggu sebentar..."
    )

async def closed_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /closed_ticket"""
    logger.info("✅ Closed Ticket command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_CLOSED_TICKET, 
        "closed_ticket.png", 
        config.CROP_DEFAULT, 
        "✅ Closed Ticket",
        "✅ Memuat Closed Ticket...\nMohon tunggu sebentar..."
    )

async def unspec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /unspec"""
    logger.info("⚠️ UNSPEC command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_UNSPEC, 
        "unspec.png", 
        config.CROP_DEFAULT, 
        "⚠️ UNSPEC",
        "⚠️ Memuat UNSPEC...\nMohon tunggu sebentar..."
    )

# HSA Commands
async def hsa_kepanjen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_kepanjen"""
    logger.info("🏢 HSA Kepanjen command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_kepanjen.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Kepanjen",
        "🏢 Memuat HSA Kepanjen...\nMohon tunggu sebentar..."
    )

async def hsa_blimbing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_blimbing"""
    logger.info("🏢 HSA Blimbing command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_blimbing.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Blimbing",
        "🏢 Memuat HSA Blimbing...\nMohon tunggu sebentar..."
    )

async def hsa_batu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_batu"""
    logger.info("🏢 HSA Batu command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_batu.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Batu",
        "🏢 Memuat HSA Batu...\nMohon tunggu sebentar..."
    )

async def hsa_klojen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_klojen"""
    logger.info("🏢 HSA Klojen command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_klojen.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Klojen",
        "🏢 Memuat HSA Klojen...\nMohon tunggu sebentar..."
    )

async def hsa_malang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_malang"""
    logger.info("🏢 HSA Malang command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_malang.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Malang",
        "🏢 Memuat HSA Malang...\nMohon tunggu sebentar..."
    )

async def hsa_singosari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_singosari"""
    logger.info("🏢 HSA Singosari command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_singosari.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Singosari",
        "🏢 Memuat HSA Singosari...\nMohon tunggu sebentar..."
    )

async def hsa_turen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_turen"""
    logger.info("🏢 HSA Turen command dipanggil")
    await handle_screenshot_command(
        update, context, 
        config.LOOKER_STUDIO_MONITORING, 
        "hsa_turen.png", 
        config.CROP_MONITORING, 
        "🏢 HSA Turen",
        "🏢 Memuat HSA Turen...\nMohon tunggu sebentar..."
    )

# Callback handlers for menu buttons
async def monitoring_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Monitoring Ticket di menu"""
    logger.info("📊 Monitoring Ticket callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_MONITORING,
        filename="monitoring.png",
        crop_config=config.CROP_MONITORING,
        caption="📊 Monitoring Ticket",
        loading_text="📊 Memuat Monitoring Ticket...\nMohon tunggu sebentar...",
        back_menu="menu_monitoring"
    )

async def closed_ticket_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Closed Ticket di menu"""
    logger.info("✅ Closed Ticket callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_CLOSED_TICKET,
        filename="closed_ticket.png",
        crop_config=config.CROP_DEFAULT,
        caption="✅ Closed Ticket",
        loading_text="✅ Memuat Closed Ticket...\nMohon tunggu sebentar...",
        back_menu="menu_assurance"
    )

async def unspec_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol UNSPEC di menu"""
    logger.info("⚠️ UNSPEC callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_UNSPEC,
        filename="unspec.png",
        crop_config=config.CROP_DEFAULT,
        caption="⚠️ UNSPEC",
        loading_text="⚠️ Memuat UNSPEC...\nMohon tunggu sebentar...",
        back_menu="menu_assurance"
    )

async def hsa_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, hsa_name: str):
    """Generic callback handler untuk HSA buttons"""
    hsa_display_name = f"HSA {hsa_name.title()}"
    logger.info(f"🏢 {hsa_display_name} callback dipanggil")
    await handle_screenshot_callback(
        update, context,
        url=config.LOOKER_STUDIO_MONITORING,
        filename=f"hsa_{hsa_name.lower()}.png",
        crop_config=config.CROP_MONITORING,
        caption=f"🏢 {hsa_display_name}",
        loading_text=f"🏢 Memuat {hsa_display_name}...\nMohon tunggu sebentar...",
        back_menu="menu_monitoring"
    )
