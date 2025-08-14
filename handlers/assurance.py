import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
import config 
from utils.assurance import take_monitoring_ticket_screenshot, take_monitoring_ticket_per_hsa_screenshot, take_closed_ticket_screenshot, take_unspec_screenshot
from utils.helpers import send_report_with_loading_cleanup
from .base import handle_screenshot_command

logger = logging.getLogger(__name__)

# Command handler for monitoring ticket
async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("🔧 Monitoring command dipanggil")
    loading_msg = await update.message.reply_text("Memuat Laporan Monitoring Ticket.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info("🔧 Mulai screenshot monitoring ticket dengan fungsi khusus")
        # Gunakan fungsi khusus monitoring ticket
        path = await take_monitoring_ticket_screenshot("monitoring_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"🔧 Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📊 Laporan Monitoring Ticket")
            os.remove(path)
            logger.info("🔧 Monitoring command selesai")
        else:
            logger.error("🔧 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🔧 Error di monitoring handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan laporan Monitoring Ticket.\nMohon coba lagi.")

async def closed_ticket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("📋 Closed Ticket command dipanggil")
    loading_msg = await update.message.reply_text("Memuat Laporan Closed Ticket.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info("📋 Mulai screenshot closed ticket dengan fungsi khusus")
        # Gunakan fungsi khusus closed ticket
        path = await take_closed_ticket_screenshot("closed_ticket.png")
        
        if path and os.path.exists(path):
            logger.info(f"📋 Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="📋 Laporan Closed Ticket")
            os.remove(path)
            logger.info("📋 Closed Ticket command selesai")
        else:
            logger.error("📋 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan laporan Closed Ticket.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"📋 Error di closed ticket handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan laporan Closed Ticket.\nMohon coba lagi.")

async def unspec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("⚠️ UNSPEC command dipanggil")
    loading_msg = await update.message.reply_text("Memuat Laporan UNSPEC.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info("⚠️ Mulai screenshot unspec dengan fungsi khusus")
        # Gunakan fungsi khusus unspec
        path = await take_unspec_screenshot("unspec.png")
        
        if path and os.path.exists(path):
            logger.info(f"⚠️ Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption="⚠️ Laporan UNSPEC")
            os.remove(path)
            logger.info("⚠️ UNSPEC command selesai")
        else:
            logger.error("⚠️ Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text("❌ Gagal menampilkan laporan UNSPEC.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"⚠️ Error di UNSPEC handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text("❌ Gagal menampilkan laporan UNSPEC.\nMohon coba lagi.")

# Command handlers untuk monitoring ticket per HSA
async def hsa_kepanjen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA KEPANJEN", "📊 Laporan Monitoring Ticket - HSA KEPANJEN")

async def hsa_blimbing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA BLIMBING", "📊 Laporan Monitoring Ticket - HSA BLIMBING")

async def hsa_batu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA BATU", "📊 Laporan Monitoring Ticket - HSA BATU")

async def hsa_klojen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA KLOJEN", "📊 Laporan Monitoring Ticket - HSA KLOJEN")

async def hsa_malang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA MALANG", "📊 Laporan Monitoring Ticket - HSA MALANG")

async def hsa_singosari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA SINGOSARI", "📊 Laporan Monitoring Ticket - HSA SINGOSARI")

async def hsa_turen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await monitoring_per_hsa(update, context, "HSA TUREN", "📊 Laporan Monitoring Ticket - HSA TUREN")

# Helper function untuk monitoring per HSA
async def monitoring_per_hsa(update: Update, context: ContextTypes.DEFAULT_TYPE, hsa_name: str, caption: str):
    logger.info(f"🔧 Monitoring {hsa_name} command dipanggil")
    loading_msg = await update.message.reply_text(f"Memuat Laporan Monitoring Ticket {hsa_name}.\nMohon Tunggu Sebentar...", parse_mode="Markdown")

    try:
        logger.info(f"🔧 Mulai screenshot monitoring ticket untuk {hsa_name}")
        # Gunakan fungsi khusus monitoring ticket per HSA
        filename = f"monitoring_ticket_{hsa_name.lower().replace('hsa ', '').replace(' ', '_')}.png"
        path = await take_monitoring_ticket_per_hsa_screenshot(hsa_name, filename)
        
        if path and os.path.exists(path):
            logger.info(f"🔧 Screenshot berhasil: {path}")
            # Hapus pesan loading dulu
            await loading_msg.delete()
            await asyncio.sleep(0.5)  # Delay kecil untuk memastikan pesan terhapus
            
            # Baru kirim foto
            with open(path, "rb") as f:
                await update.message.reply_photo(f, caption=caption)
            os.remove(path)
            logger.info(f"🔧 Monitoring {hsa_name} command selesai")
        else:
            logger.error("🔧 Screenshot gagal atau file tidak ada")
            await loading_msg.delete()
            await update.message.reply_text(f"❌ Gagal menampilkan laporan Monitoring Ticket {hsa_name}.\nMohon coba lagi.")
    except Exception as e:
        logger.error(f"🔧 Error di monitoring {hsa_name} handler: {e}")
        try:
            await loading_msg.delete()
        except:
            pass
        await update.message.reply_text(f"❌ Gagal menampilkan laporan Monitoring Ticket {hsa_name}.\nMohon coba lagi.")
