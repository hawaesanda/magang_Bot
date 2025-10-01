import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
import utils
from utils.assurance import take_monitoring_ticket_screenshot, take_monitoring_ticket_per_hsa_screenshot, take_closed_ticket_screenshot, take_unspec_screenshot
from .base import handle_screenshot_command, handle_screenshot_callback

logger = logging.getLogger(__name__)

# Command handlers (existing)
async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /monitoring_ticket"""
    logger.info("📊 Monitoring Ticket command dipanggil")
    loading_msg = await update.message.reply_text("📊 Memuat Monitoring Ticket...\nMohon tunggu sebentar...", parse_mode="Markdown")

    try:
        logger.info("📊 Mulai screenshot monitoring ticket dengan fungsi khusus")
        path = await take_monitoring_ticket_screenshot("monitoring_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"📊 Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📊 Monitoring Ticket")
            os.remove(path)
            logger.info("📊 Monitoring command selesai")
        else:
            logger.error("📊 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan Monitoring Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📊 Error di monitoring handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan Monitoring Ticket.\nMohon coba lagi.")

async def closed_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /closed_ticket"""
    logger.info("✅ Closed Ticket command dipanggil")
    loading_msg = await update.message.reply_text("✅ Memuat Closed Ticket...\nMohon tunggu sebentar...", parse_mode="Markdown")

    try:
        logger.info("✅ Mulai screenshot closed ticket dengan fungsi khusus")
        path = await take_closed_ticket_screenshot("closed_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"✅ Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="✅ Closed Ticket")
            os.remove(path)
            logger.info("✅ Closed Ticket command selesai")
        else:
            logger.error("✅ Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan Closed Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"✅ Error di closed ticket handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan Closed Ticket.\nMohon coba lagi.")

async def unspec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /unspec"""
    logger.info("⚠️ UNSPEC command dipanggil")
    loading_msg = await update.message.reply_text("⚠️ Memuat UNSPEC...\nMohon tunggu sebentar...", parse_mode="Markdown")

    try:
        logger.info("⚠️ Mulai screenshot unspec dengan fungsi khusus")
        path = await take_unspec_screenshot("unspec.png")
        
        if path and os.path.exists(path):
            logger.info(f"⚠️ Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="⚠️ UNSPEC")
            os.remove(path)
            logger.info("⚠️ UNSPEC command selesai")
        else:
            logger.error("⚠️ Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan UNSPEC.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"⚠️ Error di UNSPEC handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan UNSPEC.\nMohon coba lagi.")

# HSA Commands - Updated to use specific HSA screenshot function
async def hsa_kepanjen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_kepanjen"""
    await monitoring_per_hsa(update, context, "HSA KEPANJEN", "🏢 HSA Kepanjen")

async def hsa_blimbing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_blimbing"""
    await monitoring_per_hsa(update, context, "HSA BLIMBING", "🏢 HSA Blimbing")

async def hsa_batu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_batu"""
    await monitoring_per_hsa(update, context, "HSA BATU", "🏢 HSA Batu")

async def hsa_klojen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_klojen"""
    await monitoring_per_hsa(update, context, "HSA KLOJEN", "🏢 HSA Klojen")

async def hsa_malang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_malang"""
    await monitoring_per_hsa(update, context, "HSA MALANG", "🏢 HSA Malang")

async def hsa_singosari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_singosari"""
    await monitoring_per_hsa(update, context, "HSA SINGOSARI", "🏢 HSA Singosari")

async def hsa_turen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /hsa_turen"""
    await monitoring_per_hsa(update, context, "HSA TUREN", "🏢 HSA Turen")

# Helper function untuk monitoring per HSA
async def monitoring_per_hsa(update: Update, context: ContextTypes.DEFAULT_TYPE, hsa_name: str, caption: str):
    """Helper function untuk screenshot monitoring per HSA"""
    logger.info(f"🏢 Monitoring {hsa_name} command dipanggil")
    loading_msg = await update.message.reply_text(f"🏢 Memuat {caption}...\nMohon tunggu sebentar...", parse_mode="Markdown")

    try:
        logger.info(f"🏢 Mulai screenshot monitoring ticket untuk {hsa_name}")
        filename = f"hsa_{hsa_name.lower().replace('hsa ', '').replace(' ', '_')}.png"
        path = await take_monitoring_ticket_per_hsa_screenshot(hsa_name, filename)
        
        if path and os.path.exists(path):
            logger.info(f"🏢 Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption=caption)
            os.remove(path)
            logger.info(f"🏢 Monitoring {hsa_name} command selesai")
        else:
            logger.error("🏢 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text(f"❌ Gagal menampilkan {caption}.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🏢 Error di monitoring {hsa_name} handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Gagal menampilkan {caption}.\nMohon coba lagi.")

# Callback handlers for menu buttons
async def monitoring_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Monitoring Ticket di menu"""
    logger.info("📊 Monitoring Ticket callback dipanggil")
    query = update.callback_query
    await query.answer()
    
    loading_msg = await query.edit_message_text("📊 Memuat Monitoring Ticket...\nMohon tunggu sebentar...")

    try:
        logger.info("📊 Mulai screenshot monitoring ticket dengan fungsi khusus")
        path = await take_monitoring_ticket_screenshot("monitoring_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"📊 Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await query.message.reply_photo(f, caption="📊 Monitoring Ticket")
            os.remove(path)
            logger.info("📊 Monitoring callback selesai")
        else:
            logger.error("📊 Screenshot gagal atau file tidak ada")
            await loading_msg.edit_text("❌ Gagal menampilkan Monitoring Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📊 Error di monitoring callback: {e}")
        try:
            await loading_msg.edit_text("❌ Gagal menampilkan Monitoring Ticket.\nMohon coba lagi.")
        except:
            pass

async def closed_ticket_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol Closed Ticket di menu"""
    logger.info("✅ Closed Ticket callback dipanggil")
    query = update.callback_query
    await query.answer()
    
    loading_msg = await query.edit_message_text("✅ Memuat Closed Ticket...\nMohon tunggu sebentar...")

    try:
        logger.info("✅ Mulai screenshot closed ticket dengan fungsi khusus")
        path = await take_closed_ticket_screenshot("closed_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"✅ Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await query.message.reply_photo(f, caption="✅ Closed Ticket")
            os.remove(path)
            logger.info("✅ Closed Ticket callback selesai")
        else:
            logger.error("✅ Screenshot gagal atau file tidak ada")
            await loading_msg.edit_text("❌ Gagal menampilkan Closed Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"✅ Error di closed ticket callback: {e}")
        try:
            await loading_msg.edit_text("❌ Gagal menampilkan Closed Ticket.\nMohon coba lagi.")
        except:
            pass

async def unspec_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback handler untuk tombol UNSPEC di menu"""
    logger.info("⚠️ UNSPEC callback dipanggil")
    query = update.callback_query
    await query.answer()
    
    loading_msg = await query.edit_message_text("⚠️ Memuat UNSPEC...\nMohon tunggu sebentar...")

    try:
        logger.info("⚠️ Mulai screenshot unspec dengan fungsi khusus")
        path = await take_unspec_screenshot("unspec.png")
        
        if path and os.path.exists(path):
            logger.info(f"⚠️ Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await query.message.reply_photo(f, caption="⚠️ UNSPEC")
            os.remove(path)
            logger.info("⚠️ UNSPEC callback selesai")
        else:
            logger.error("⚠️ Screenshot gagal atau file tidak ada")
            await loading_msg.edit_text("❌ Gagal menampilkan UNSPEC.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"⚠️ Error di UNSPEC callback: {e}")
        try:
            await loading_msg.edit_text("❌ Gagal menampilkan UNSPEC.\nMohon coba lagi.")
        except:
            pass

async def hsa_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, hsa_name: str):
    """Generic callback handler untuk HSA buttons"""
    hsa_display_name = f"HSA {hsa_name.title()}"
    full_hsa_name = f"HSA {hsa_name.upper()}"
    logger.info(f"🏢 {hsa_display_name} callback dipanggil")
    query = update.callback_query
    await query.answer()
    
    loading_msg = await query.edit_message_text(f"🏢 Memuat {hsa_display_name}...\nMohon tunggu sebentar...")

    try:
        logger.info(f"🏢 Mulai screenshot monitoring ticket untuk {full_hsa_name}")
        filename = f"hsa_{hsa_name.lower()}.png"
        path = await take_monitoring_ticket_per_hsa_screenshot(full_hsa_name, filename)
        
        if path and os.path.exists(path):
            logger.info(f"🏢 Screenshot berhasil: {path}")
            await loading_msg.delete()
            await asyncio.sleep(0.5)
            
            with open(path, "rb") as f:
                await query.message.reply_photo(f, caption=f"🏢 {hsa_display_name}")
            os.remove(path)
            logger.info(f"🏢 {hsa_display_name} callback selesai")
        else:
            logger.error("🏢 Screenshot gagal atau file tidak ada")
            await loading_msg.edit_text(f"❌ Gagal menampilkan {hsa_display_name}.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🏢 Error di {hsa_display_name} callback: {e}")
        try:
            await loading_msg.edit_text(f"❌ Gagal menampilkan {hsa_display_name}.\nMohon coba lagi.")
        except:
            pass
