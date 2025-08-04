"""
Handler khusus untuk screenshot section tertentu dari dashboard
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
import config
from utils import get_section_screenshot, get_screenshot_by_element

logger = logging.getLogger(__name__)

# --- Handler untuk screenshot section MSA ---
async def msa_fulfillment_fbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot section Fulfillment FBB saja"""
    try:
        await update.message.reply_text("📸 Mengambil screenshot section Fulfillment FBB...")
        
        current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
        filename = f"msa_fulfillment_fbb_{current_time}.png"
        
        result = await get_section_screenshot(
            config.LOOKER_STUDIO_MSA_WSA_URL,
            filename,
            "FULFILLMENT_FBB"
        )
        
        if result:
            with open(result, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📊 MSA - Fulfillment FBB")
        else:
            await update.message.reply_text("❌ Gagal mengambil screenshot section.")
            
    except Exception as e:
        logger.error(f"Error di msa_fulfillment_fbb: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")

async def msa_assurance_fbb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot section Assurance FBB saja"""
    try:
        await update.message.reply_text("📸 Mengambil screenshot section Assurance FBB...")
        
        current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
        filename = f"msa_assurance_fbb_{current_time}.png"
        
        result = await get_section_screenshot(
            config.LOOKER_STUDIO_MSA_WSA_URL,
            filename,
            "ASSURANCE_FBB"
        )
        
        if result:
            with open(result, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📊 MSA - Assurance FBB")
        else:
            await update.message.reply_text("❌ Gagal mengambil screenshot section.")
            
    except Exception as e:
        logger.error(f"Error di msa_assurance_fbb: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")

async def msa_quality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot section MSA Quality saja"""
    try:
        await update.message.reply_text("📸 Mengambil screenshot section MSA Quality...")
        
        current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
        filename = f"msa_quality_{current_time}.png"
        
        result = await get_section_screenshot(
            config.LOOKER_STUDIO_MSA_WSA_URL,
            filename,
            "MSA_QUALITY"
        )
        
        if result:
            with open(result, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📊 MSA - Quality")
        else:
            await update.message.reply_text("❌ Gagal mengambil screenshot section.")
            
    except Exception as e:
        logger.error(f"Error di msa_quality: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")

# --- Handler untuk monitoring ticket sections ---
async def monitoring_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot bagian atas monitoring ticket"""
    try:
        await update.message.reply_text("📸 Mengambil screenshot monitoring ticket (bagian atas)...")
        
        current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
        filename = f"monitoring_top_{current_time}.png"
        
        result = await get_section_screenshot(
            config.LOOKER_STUDIO_MONITORING,
            filename,
            "MONITORING_TOP"
        )
        
        if result:
            with open(result, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📊 Monitoring Ticket - Bagian Atas")
        else:
            await update.message.reply_text("❌ Gagal mengambil screenshot section.")
            
    except Exception as e:
        logger.error(f"Error di monitoring_top: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")

async def monitoring_middle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot bagian tengah monitoring ticket"""
    try:
        await update.message.reply_text("📸 Mengambil screenshot monitoring ticket (bagian tengah)...")
        
        current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
        filename = f"monitoring_middle_{current_time}.png"
        
        result = await get_section_screenshot(
            config.LOOKER_STUDIO_MONITORING,
            filename,
            "MONITORING_MIDDLE"
        )
        
        if result:
            with open(result, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📊 Monitoring Ticket - Bagian Tengah")
        else:
            await update.message.reply_text("❌ Gagal mengambil screenshot section.")
            
    except Exception as e:
        logger.error(f"Error di monitoring_middle: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")

async def monitoring_bottom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot bagian bawah monitoring ticket"""
    try:
        await update.message.reply_text("📸 Mengambil screenshot monitoring ticket (bagian bawah)...")
        
        current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
        filename = f"monitoring_bottom_{current_time}.png"
        
        result = await get_section_screenshot(
            config.LOOKER_STUDIO_MONITORING,
            filename,
            "MONITORING_BOTTOM"
        )
        
        if result:
            with open(result, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption="📊 Monitoring Ticket - Bagian Bawah")
        else:
            await update.message.reply_text("❌ Gagal mengambil screenshot section.")
            
    except Exception as e:
        logger.error(f"Error di monitoring_bottom: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")

# --- Handler untuk screenshot dengan custom section ---
async def custom_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Screenshot section custom berdasarkan input user"""
    try:
        # Ambil section name dari argument
        if context.args:
            section_name = " ".join(context.args).upper()
            await update.message.reply_text(f"📸 Mengambil screenshot section: {section_name}...")
            
            current_time = datetime.now(config.TIMEZONE).strftime("%d%m%Y_%H%M")
            filename = f"custom_section_{current_time}.png"
            
            # Coba dengan MSA URL dulu
            result = await get_section_screenshot(
                config.LOOKER_STUDIO_MSA_WSA_URL,
                filename,
                section_name
            )
            
            if result:
                with open(result, 'rb') as photo:
                    await update.message.reply_photo(photo=photo, caption=f"📊 {section_name}")
            else:
                await update.message.reply_text("❌ Section tidak ditemukan atau gagal mengambil screenshot.")
        else:
            await update.message.reply_text(
                "ℹ️ Gunakan: /custom_section [nama_section]\n\n"
                "Contoh: /custom_section FULFILLMENT_FBB\n\n"
                "Section tersedia:\n"
                "• FULFILLMENT_FBB\n"
                "• ASSURANCE_FBB\n"
                "• SCORE_CREDIT\n"
                "• FULFILLMENT_BGES\n"
                "• ASSURANCE_BGES\n"
                "• MSA_ASSURANCE\n"
                "• MSA_CNOP\n"
                "• MSA_QUALITY\n"
                "• MONITORING_TOP\n"
                "• MONITORING_MIDDLE\n"
                "• MONITORING_BOTTOM"
            )
            
    except Exception as e:
        logger.error(f"Error di custom_section: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat mengambil screenshot.")
